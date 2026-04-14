import streamlit as st

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.sheets import get_stock_data, write_order
from backend.price_parser import get_price, load_prices_from_drive
from backend.pdf_generator import generate_pdf
from backend.drive_upload import upload_file
import datetime



load_prices_from_drive()


st.title("Interio Order Booking")

name = st.text_input("Customer Name")
phone = st.text_input("Phone")
address = st.text_area("Address")

stock = get_stock_data()


items = {i["Item code"]: i["Item Description"] for i in stock}

item_code = st.selectbox("Select Item", list(items.keys()))
item_name = items[item_code]

qty = st.number_input("Quantity", min_value=1)

salesperson = st.text_input("Your Email")

if st.button("Create Order"):

    price = get_price(item_code)
    total = price * qty

    order_id = "ORD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    order_data = {
        "customer_name": name,
        "phone": phone,
        "address": address,
        "item_name": item_name,
        "qty": qty,
        "price": price,
        "total": total
    }

    pdf_file = f"{order_id}.pdf"
    generate_pdf(order_data, pdf_file)

    pdf_link = upload_file(pdf_file)

    write_order([
        str(datetime.date.today()),
        order_id,
        name,
        phone,
        address,
        item_code,
        item_name,
        qty,
        price,
        total,
        salesperson,
        pdf_link
    ])

    st.success("Order Created!")
    st.write(pdf_link)