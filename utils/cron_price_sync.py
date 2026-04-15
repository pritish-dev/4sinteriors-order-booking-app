from services.drive import get_pdfs, download_pdf
from services.gemini_parser import extract_price_with_gemini
from services.sheets import client
import pandas as pd
import streamlit as st

files = get_pdfs()

final_df = pd.DataFrame()

for f in files:
    pdf = download_pdf(f["id"])
    df = extract_price_with_gemini(pdf)
    final_df = pd.concat([final_df, df])

sheet = client.open_by_key(st.secrets["STOCK_SHEET_ID"]).worksheet("Price_list")

sheet.clear()
sheet.append_row(["LN_CODE", "MRP"])

for row in final_df.values.tolist():
    sheet.append_row(row)

print("✅ Daily Price Sync Completed")