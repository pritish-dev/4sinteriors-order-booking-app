import gspread
import os
import json
import streamlit as st
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)


def get_stock():
    sheet = client.open_by_key(os.environ["STOCK_SHEET_ID"]).worksheet("STOCK")
    return sheet.get_all_records()


def get_price_map():
    sheet = client.open_by_key(os.environ["STOCK_SHEET_ID"]).worksheet(os.environ["PRICE_SHEET_NAME"])
    data = sheet.get_all_records()
    return {str(i["LN_CODE"]).strip(): int(i["MRP"]) for i in data}


def write_order(row):
    sheet = client.open_by_key(os.environ["ORDER_SHEET_ID"]).worksheet("Franchise Orders")
    sheet.append_row(row)


def update_price_sheet(df):
    sheet = client.open_by_key(os.environ["STOCK_SHEET_ID"]).worksheet(os.environ["PRICE_SHEET_NAME"])
    sheet.clear()
    sheet.append_row(["LN_CODE", "MRP"])

    for row in df.values.tolist():
        sheet.append_row(row)