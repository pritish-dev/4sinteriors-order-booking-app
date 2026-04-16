import streamlit as st
import datetime
import pandas as pd

from utils.auth import login, check_auth

from services.sheets import (
    get_stock,
    write_order,
    get_price_map
)
try:
    from services.sheets import update_price_sheet
except:
    update_price_sheet = None
from services.pdf_generator import generate_pdf
from services.whatsapp import generate_whatsapp_link

# ✅ FIXED IMPORTS (THIS SOLVES YOUR ERROR)
from services.drive import get_pdfs, download_pdf
from services.gemini_parser import extract_price_with_gemini


# ---------- LOGIN ----------
if not check_auth():
    login()
    st.stop()

user = st.session_state["user"]

st.title(f"🪑 Order Booking - {user.get('name')}")

# ---------- 🔄 PRICE UPDATE ----------
st.markdown("## 🔄 Price List Management")

if st.button("Update Price List from PDFs"):

    files = get_pdfs()   # ✅ NOW WORKS

    if not files:
        st.warning("No PDF files found in Drive")

    else:
        all_data = []

        for file in files:
            st.write(f"Processing: {file['name']}")

            pdf = download_pdf(file["id"])
            df = extract_price_with_gemini(pdf)

            if not df.empty:
                all_data.append(df)

        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)
            update_price_sheet(final_df)
            st.success("✅ Price sheet updated!")
        else:
            st.error("❌ No data extracted")


# ---------- LOAD DATA ----------
stock_df = get_stock()
price_map = get_price_map()


# ---------- CUSTOMER ----------
customer_name = st.text_input("Customer Name")
phone = st.text_input("Phone")


# ---------- ITEMS ----------
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

    qty = st.number_input("Qty", 1, 100, 1, key=f"qty_{i}")

    st.write(f"💰 Price: ₹{price}")
    st.write(f"📦 Stock: {selected.get('FREE_STOCK')}")
    st.write(f"🏬 WH: {selected.get('WAREHOUSE_CODE')}")

    items.append({
        "name": item_name,
        "code": item_code,
        "qty": qty,
        "price": price,
        "warehouse": selected.get("WAREHOUSE_CODE")
    })


# ---------- TOTAL ----------
total = sum(i["qty"] * i["price"] for i in items)
st.success(f"Total: ₹{total}")


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

    file_name = f"{order_id}.pdf"
    generate_pdf({"items": items}, file_name)

    st.success("✅ Order Created")

    with open(file_name, "rb") as f:
        st.download_button("Download PDF", f)

    wa_link = generate_whatsapp_link(phone, f"Order Total ₹{total}")
    st.markdown(f"[Send WhatsApp]({wa_link})")