import streamlit as st
from services.sheets import get_stock, get_price_map, write_order
from services.drive import get_pdfs, download_pdf
from services.pdf_to_sheet import extract_pdf_to_dataframe
from services.pdf_generator import generate_pdf
import datetime
from services.gemini_parser import extract_price_with_gemini
from services.sheets import client
import pandas as pd

st.title("Interio Order App")

# 🔥 Load Data
stock = get_stock()
price_map = get_price_map()

items = {i["Item code"]: i["Item Description"] for i in stock}

# UI
name = st.text_input("Customer Name")
phone = st.text_input("Phone")

item_code = st.selectbox("Item", list(items.keys()))
qty = st.number_input("Qty", 1)

price = price_map.get(item_code, 0)
total = price * qty

st.write("Price:", price)
st.write("Total:", total)

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

    st.success("Order Created ✅")



if st.button("🔄 Sync Price (AI Powered)"):
    files = get_pdfs()

    final_df = pd.DataFrame()

    for f in files:
        pdf = download_pdf(f["id"])
        df = extract_price_with_gemini(pdf)
        final_df = pd.concat([final_df, df])

    sheet = client.open_by_key(st.secrets["STOCK_SHEET_ID"]).worksheet("Price_list")

    sheet.clear()
    sheet.append_row(["LN_CODE", "MRP"])

    for row in final_df.values.tolist():
        sheet.append_row(row)

    st.success("✅ AI Price Sync Completed")