import pdfplumber
import os

PRICE_CACHE = {}


def load_prices_from_folder(folder="price_files"):
    global PRICE_CACHE
    PRICE_CACHE = {}

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)

            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        for row in table:
                            try:
                                ln_code = str(row[1]).strip()
                                mrp = int(str(row[-1]).replace(",", ""))
                                PRICE_CACHE[ln_code] = mrp
                            except:
                                continue

    return PRICE_CACHE


def get_price(item_code):
    return PRICE_CACHE.get(item_code, 0)