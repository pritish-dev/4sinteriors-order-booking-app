import streamlit as st
import datetime

from utils.auth import login, check_auth
from services.sheets import get_stock, write_order
from services.pdf_generator import generate_pdf
from services.whatsapp import generate_whatsapp_link

# ---------- LOGIN ----------
if not check_auth():
    login()
    st.stop()

user = st.session_state["user"]

st.title(f"🪑 Order Booking - {user.get('name')}")

# ---------- LOAD STOCK ----------
stock_df = get_stock()

# DEBUG (remove later)
# st.write(stock_df.columns)

# ---------- SAFETY CHECK ----------
required_cols = ["ITEM_NAME", "ITEM_CODE", "PRICE", "STOCK", "WAREHOUSE"]

for col in required_cols:
    if col not in stock_df.columns:
        st.error(f"❌ Missing column: {col} in STOCK sheet")
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
        stock_df["ITEM_NAME"].dropna().unique().tolist(),
        key=f"item_{i}"
    )

    selected = stock_df[stock_df["ITEM_NAME"] == item_name].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        qty = st.number_input("Qty", 1, 100, 1, key=f"qty_{i}")

    with col2:
        price = int(selected.get("PRICE", 0))
        st.write(f"💰 Price: ₹{price}")

    with col3:
        st.write(f"📦 Stock: {selected.get('STOCK', 0)}")
        st.write(f"🏬 WH: {selected.get('WAREHOUSE', '')}")

    items.append({
        "name": item_name,
        "code": selected.get("ITEM_CODE"),
        "qty": qty,
        "price": price,
        "warehouse": selected.get("WAREHOUSE")
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