import gspread
import json
import pandas as pd
from google.oauth2.service_account import Credentials
from utils.config import get_secret

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(get_secret("GOOGLE_SERVICE_ACCOUNT"))
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)


# ✅ Normalize column names
def normalize_df(df):
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
    return df


# ✅ Fetch stock
def get_stock():
    sheet = client.open_by_key(get_secret("STOCK_SHEET_ID")).worksheet("STOCK")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return normalize_df(df)


# ✅ Fetch users
def get_users():
    sheet = client.open_by_key(get_secret("STOCK_SHEET_ID")).worksheet("USERS")
    return sheet.get_all_records()


# ✅ Write order
def write_order(row):
    sheet = client.open_by_key(get_secret("ORDER_SHEET_ID")).worksheet("Franchise Orders")
    sheet.append_row(row)


# ✅ Optional price map (if using price sheet)
def get_price_map():
    try:
        sheet = client.open_by_key(get_secret("STOCK_SHEET_ID")).worksheet("PRICE_SHEET")
        data = sheet.get_all_records()

        price_map = {}
        for row in data:
            code = str(row.get("LN_CODE")).strip()
            price = float(row.get("MRP", 0))
            price_map[code] = price

        return price_map
    except:
        return {}