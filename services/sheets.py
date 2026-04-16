import gspread
import json
from google.oauth2.service_account import Credentials
from utils.config import get_secret

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(get_secret("GOOGLE_SERVICE_ACCOUNT"))

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)


def get_stock():
    sheet = client.open_by_key(get_secret("STOCK_SHEET_ID")).worksheet("STOCK")
    data = sheet.get_all_records()
    
    import pandas as pd
    df = pd.DataFrame(data)

    # 🔥 Normalize columns
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]

    return df


def get_price_map():
    sheet_name = get_secret("PRICE_SHEET_NAME") or "PRICE_SHEET"

    sheet = client.open_by_key(
        get_secret("STOCK_SHEET_ID")
    ).worksheet(sheet_name.strip())

    data = sheet.get_all_records()

    return {
        str(i["LN_CODE"]).strip(): int(i["MRP"])
        for i in data if i.get("LN_CODE")
    }


def write_order(row):
    sheet = client.open_by_key(get_secret("ORDER_SHEET_ID")).worksheet("Franchise Orders")
    sheet.append_row(row)


def update_price_sheet(df):
    sheet_name = get_secret("PRICE_SHEET_NAME") or "PRICE_SHEET"

    sheet = client.open_by_key(
        get_secret("STOCK_SHEET_ID")
    ).worksheet(sheet_name.strip())

    sheet.clear()
    sheet.append_row(["LN_CODE", "MRP"])

    for row in df.values.tolist():
        sheet.append_row(row)

def get_users():
    sheet = client.open_by_key(get_secret("STOCK_SHEET_ID")).worksheet("USERS")
    data = sheet.get_all_records()
    return data