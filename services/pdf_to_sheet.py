import pdfplumber
import pandas as pd


def extract_pdf_to_dataframe(file_bytes):
    rows = []

    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    try:
                        ln_code = str(row[1]).strip()
                        mrp = int(str(row[-1]).replace(",", ""))
                        rows.append([ln_code, mrp])
                    except:
                        continue

    return pd.DataFrame(rows, columns=["LN_CODE", "MRP"])