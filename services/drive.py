import io
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from utils.config import get_secret

creds_dict = json.loads(get_secret("GOOGLE_SERVICE_ACCOUNT"))

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive = build("drive", "v3", credentials=creds)


def get_pdfs():
    folder_id = get_secret("DRIVE_FOLDER_ID")

    results = drive.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/pdf'",
        fields="files(id, name)"
    ).execute()

    return results.get("files", [])


def download_pdf(file_id):
    request = drive.files().get_media(fileId=file_id)
    return io.BytesIO(request.execute())