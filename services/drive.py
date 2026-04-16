import io
import json
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from utils.config import get_secret

scope = ["https://www.googleapis.com/auth/drive"]

creds_dict = json.loads(get_secret("GOOGLE_SERVICE_ACCOUNT"))
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

drive_service = build("drive", "v3", credentials=creds)


def get_pdfs():
    folder_id = get_secret("DRIVE_FOLDER_ID")

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/pdf'",
        fields="files(id, name)"
    ).execute()

    return results.get("files", [])


def download_pdf(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    file.seek(0)
    return file