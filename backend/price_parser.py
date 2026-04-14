import pdfplumber
import io
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from backend.config import *

PRICE_CACHE = {}

# Setup Drive API
scope = ["https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
drive_service = build('drive', 'v3', credentials=creds)


def load_prices_from_drive():
    global PRICE_CACHE
    PRICE_CACHE = {}

    print("📂 Fetching PDFs from Google Drive...")

    results = drive_service.files().list(
        q=f"'{DRIVE_FOLDER_ID}' in parents and mimeType='application/pdf'",
        fields="files(id, name)"
    ).execute()

    files = results.get('files', [])

    if not files:
        print("⚠️ No PDF files found in Drive folder")
        return PRICE_CACHE

    for file in files:
        file_id = file['id']
        file_name = file['name']

        print(f"📄 Processing: {file_name}")

        request = drive_service.files().get_media(fileId=file_id)
        file_bytes = io.BytesIO(request.execute())

        with pdfplumber.open(file_bytes) as pdf:
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

    print("✅ Prices Loaded:", len(PRICE_CACHE))
    return PRICE_CACHE


def get_price(item_code):
    return PRICE_CACHE.get(str(item_code).strip(), 0)