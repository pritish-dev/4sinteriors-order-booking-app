import streamlit as st
import pandas as pd

from utils.auth import login, check_auth
from services.sheets import get_stock, write_order
from services.pdf_generator import generate_pdf
from services.whatsapp import generate_whatsapp_link

# ---------- AUTH ----------
if not check_auth():
    login()
    st.stop()

user = st.session_state["user"]

st.title(f"🪑 Order Booking - {user['name']}")

# ---------- LOAD STOCK ----------
stock_df = get_stock()

# ---------- CUSTOMER ----------
st.subheader("Customer Details")

customer_name = st.text_input("Customer Name")
phone = st.text_input("Phone")

# ---------- MULTI ITEM ----------
st.subheader("Add Items")

items = []

num_items = st.number_input("Number of Items", 1, 10, 1)

for i in range(num_items):
    st.markdown(f"### Item {i+1}")

    item_name = st.selectbox(
        f"Search Item {i}",
        stock_df["ITEM_NAME"].tolist(),
        key=f"item_{i}"
    )

    selected = stock_df[stock_df["ITEM_NAME"] == item_name].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        qty = st.number_input("Qty", 1, 10, 1, key=f"qty_{i}")

    with col2:
        price = selected["PRICE"]
        st.text(f"Price: {price}")

    with col3:
        st.text(f"Stock: {selected['STOCK']}")

    items.append({
        "name": item_name,
        "code": selected["ITEM_CODE"],
        "qty": qty,
        "price": price,
        "warehouse": selected["WAREHOUSE"]
    })

# ---------- TOTAL ----------
total = sum(i["qty"] * i["price"] for i in items)
st.success(f"Total Amount: ₹{total}")

# ---------- SAVE ----------
if st.button("Create Order"):
    order = {
        "customer_name": customer_name,
        "phone": phone,
        "items": items,
        "salesperson": user["name"]
    }

    write_order(order)

    # Generate PDF
    pdf_file = generate_pdf(order)

    # WhatsApp message
    msg = f"""
Order Confirmed ✅
Customer: {customer_name}
Total: ₹{total}

Thank you for choosing Interio 🙏
"""

    wa_link = generate_whatsapp_link(phone, msg)

    st.success("Order Saved!")

    # Download PDF
    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download PDF", f, file_name="order.pdf")

    # WhatsApp button
    st.markdown(f"[📲 Send via WhatsApp]({wa_link})")