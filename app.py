import streamlit as st
import datetime
import pandas as pd

from services.sheets import get_stock, get_price_map, write_order, update_price_sheet
from services.drive import get_pdfs, download_pdf
from services.gemini_parser import extract_price_with_gemini
from services.pdf_generator import generate_pdf

st.set_page_config(page_title="Interio Order App", layout="wide")

st.title("🛋️ Interio Order Booking App")

# ================= PRICE SYNC =================

st.header("📄 Price List Management")

if st.button("🔄 Update Price List (Upload New PDF First)"):
    files = get_pdfs()

    if not files:
        st.error("❌ No PDF found in Drive folder")
    else:
        final_df = pd.DataFrame()

        for f in files:
            pdf = download_pdf(f["id"])
            df = extract_price_with_gemini(pdf)
            final_df = pd.concat([final_df, df])

        if not final_df.empty:
            update_price_sheet(final_df)
            st.success("✅ Price list updated successfully")
        else:
            st.error("❌ Failed to extract data from PDF")

# ================= ORDER CREATION =================

st.header("🧾 Create Order")

stock = get_stock()
price_map = get_price_map()

items = {i["Item code"]: i["Item Description"] for i in stock}

name = st.text_input("Customer Name")
phone = st.text_input("Phone")

item_code = st.selectbox("Select Item", list(items.keys()))
qty = st.number_input("Quantity", min_value=1, value=1)

price = price_map.get(item_code, 0)
total = price * qty

st.write(f"💰 Price: ₹{price}")
st.write(f"🧮 Total: ₹{total}")

if st.button("Create Order"):
    order_id = "ORD" + datetime.datetime.now().strftime("%Y%m%d%H%M")

    generate_pdf({
        "customer": name,
        "phone": phone,
        "item": items[item_code],
        "qty": qty,
        "total": total
    }, f"{order_id}.pdf")

    write_order([
        str(datetime.date.today()),
        order_id,
        name,
        phone,
        item_code,
        qty,
        total
    ])

    st.success("✅ Order Created Successfully")