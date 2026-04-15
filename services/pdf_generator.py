from reportlab.platypus import SimpleDocTemplate, Table


def generate_pdf(data, filename):
    doc = SimpleDocTemplate(filename)

    table = Table([
        ["Customer", data["customer"]],
        ["Phone", data["phone"]],
        ["Item", data["item"]],
        ["Qty", data["qty"]],
        ["Total", data["total"]],
    ])

    doc.build([table])