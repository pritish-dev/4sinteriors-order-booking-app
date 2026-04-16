import streamlit as st
import datetime

from utils.auth import login, check_auth
from services.sheets import get_stock, write_order, get_price_map
from services.pdf_generator import generate_pdf
from services.whatsapp import generate_whatsapp_link

# ---------- LOGIN ----------
if not check_auth():
    login()
    st.stop()

user = st.session_state["user"]

st.title(f"🪑 Order Booking - {user.get('name')}")

# ---------- LOAD DATA ----------
stock_df = get_stock()
price_map = get_price_map()

# ---------- CHECK REQUIRED COLUMNS ----------
required_cols = [
    "ITEM_DESCRIPTION",
    "ITEM_CODE",
    "FREE_STOCK",
    "WAREHOUSE_CODE"
]

for col in required_cols:
    if col not in stock_df.columns:
        st.error(f"❌ Missing column: {col}")
        st.stop()

# ---------- CUSTOMER ----------
st.subheader("Customer Details")

customer_name = st.text_input("Customer Name")
phone = st.text_input("Phone")

# ---------- ITEMS ----------
st.subheader("Add Items")

items = []
num_items = st.number_input("Number of Items", 1, 10, 1)

for i in range(num_items):

    item_name = st.selectbox(
        f"Search Item {i+1}",
        stock_df["ITEM_DESCRIPTION"].dropna().unique().tolist(),
        key=f"item_{i}"
    )

    selected = stock_df[stock_df["ITEM_DESCRIPTION"] == item_name].iloc[0]

    item_code = str(selected.get("ITEM_CODE")).strip()

    price = price_map.get(item_code, 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        qty = st.number_input("Qty", 1, 100, 1, key=f"qty_{i}")

    with col2:
        st.write(f"💰 Price: ₹{price}")

    with col3:
        stock = selected.get("FREE_STOCK", 0)
        st.write(f"📦 Stock: {stock}")
        st.write(f"🏬 WH: {selected.get('WAREHOUSE_CODE')}")

    # 🔥 Stock validation
    if qty > stock:
        st.error("❌ Not enough stock")

    items.append({
        "name": item_name,
        "code": item_code,
        "qty": qty,
        "price": price,
        "warehouse": selected.get("WAREHOUSE_CODE")
    })

# ---------- TOTAL ----------
total = sum(i["qty"] * i["price"] for i in items)
st.success(f"Total Amount: ₹{total}")

# ---------- CREATE ORDER ----------
if st.button("Create Order"):

    order_id = "ORD" + datetime.datetime.now().strftime("%Y%m%d%H%M")

    for item in items:
        write_order([
            str(datetime.date.today()),
            order_id,
            customer_name,
            phone,
            item["code"],
            item["name"],
            item["qty"],
            item["price"],
            item["qty"] * item["price"],
            item["warehouse"],
            user.get("name")
        ])

    # PDF
    file_name = f"{order_id}.pdf"
    generate_pdf({"items": items}, file_name)

    # WhatsApp
    msg = f"""
Order Confirmed ✅
Customer: {customer_name}
Total: ₹{total}
Thank you 🙏
"""

    wa_link = generate_whatsapp_link(phone, msg)

    st.success("✅ Order Created")

    with open(file_name, "rb") as f:
        st.download_button("📄 Download PDF", f)

    st.markdown(f"[📲 Send via WhatsApp]({wa_link})")