from fastapi import FastAPI
from backend.sheets import get_stock_data, write_order
from backend.price_parser import load_prices_from_folder, get_price
from backend.pdf_generator import generate_pdf
from backend.drive_upload import upload_file
import datetime

app = FastAPI()

# Load prices on startup
from backend.price_parser import load_prices_from_drive, get_price

@app.on_event("startup")
def startup_event():
    load_prices_from_drive()


@app.get("/stock")
def stock():
    return get_stock_data()


@app.post("/create-order")
def create_order(order: dict):

    price = get_price(order["item_code"])
    total = price * order["qty"]

    order_id = "ORD" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    order_data = {
        **order,
        "price": price,
        "total": total
    }

    pdf_file = f"{order_id}.pdf"
    generate_pdf(order_data, pdf_file)

    pdf_link = upload_file(pdf_file)

    write_order([
        str(datetime.date.today()),
        order_id,
        order["customer_name"],
        order["phone"],
        order["address"],
        order["item_code"],
        order["item_name"],
        order["qty"],
        price,
        total,
        order["salesperson"],
        pdf_link
    ])

    return {
        "status": "success",
        "pdf": pdf_link
    }