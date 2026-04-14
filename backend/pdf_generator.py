from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors


def generate_pdf(order, filename):
    doc = SimpleDocTemplate(filename)

    data = [
        ["Customer Name", order["customer_name"]],
        ["Phone", order["phone"]],
        ["Address", order["address"]],
        ["Item", order["item_name"]],
        ["Qty", order["qty"]],
        ["Price", order["price"]],
        ["Total", order["total"]],
    ]

    table = Table(data)
    table.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    doc.build([table])