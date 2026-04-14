import gspread
from google.oauth2.service_account import Credentials
from backend.config import *

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)

stock_sheet = client.open_by_key(STOCK_SHEET_ID).worksheet("STOCK")
order_sheet = client.open_by_key(ORDER_SHEET_ID).worksheet("Franchise Orders")


def get_stock_data():
    return stock_sheet.get_all_records()


def write_order(data):
    order_sheet.append_row(data)