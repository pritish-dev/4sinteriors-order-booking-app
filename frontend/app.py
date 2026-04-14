import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Interio Order Booking")

name = st.text_input("Customer Name")
phone = st.text_input("Phone")
address = st.text_area("Address")

stock = requests.get(f"{API_URL}/stock").json()

items = {i["Item code"]: i["Item Description"] for i in stock}

item_code = st.selectbox("Select Item", list(items.keys()))
item_name = items[item_code]

qty = st.number_input("Quantity", min_value=1)

salesperson = st.text_input("Your Email")

if st.button("Create Order"):
    res = requests.post(f"{API_URL}/create-order", json={
        "customer_name": name,
        "phone": phone,
        "address": address,
        "item_code": item_code,
        "item_name": item_name,
        "qty": qty,
        "salesperson": salesperson
    })

    st.success("Order Created!")
    st.write(res.json()["pdf"])