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


# 🔥 Normalize columns function
def normalize_df(df):
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
    return df


def get_stock():
    sheet = client.open_by_key(get_secret("STOCK_SHEET_ID")).worksheet("STOCK")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return normalize_df(df)


def get_users():
    sheet = client.open_by_key(get_secret("STOCK_SHEET_ID")).worksheet("USERS")
    data = sheet.get_all_records()
    return data


def write_order(row):
    sheet = client.open_by_key(get_secret("ORDER_SHEET_ID")).worksheet("Franchise Orders")
    sheet.append_row(row)