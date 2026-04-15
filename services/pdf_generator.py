from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import datetime

def generate_pdf(order):
    file_path = f"order_{datetime.datetime.now().timestamp()}.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("ORDER CONFIRMATION - INTERIO", styles["Title"]))

    elements.append(Paragraph(f"Customer: {order['customer_name']}", styles["Normal"]))
    elements.append(Paragraph(f"Phone: {order['phone']}", styles["Normal"]))

    table_data = [["Item", "Code", "Qty", "Price", "Total"]]

    total = 0

    for item in order["items"]:
        line_total = item["qty"] * item["price"]
        total += line_total

        table_data.append([
            item["name"],
            item["code"],
            item["qty"],
            item["price"],
            line_total
        ])

    table_data.append(["", "", "", "TOTAL", total])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(table)

    doc.build(elements)

    return file_path