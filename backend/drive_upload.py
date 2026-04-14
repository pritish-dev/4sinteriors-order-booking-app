from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from backend.config import *
from google.oauth2.service_account import Credentials

scope = ["https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)

service = build('drive', 'v3', credentials=creds)


def upload_file(file_path):
    file_metadata = {
        'name': file_path,
        'parents': [DRIVE_FOLDER_ID]
    }

    media = MediaFileUpload(file_path)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return f"https://drive.google.com/file/d/{file['id']}/view"