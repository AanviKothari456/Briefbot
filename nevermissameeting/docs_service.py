from googleapiclient.discovery import build
from google.oauth2 import service_account
import re

SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']
SERVICE_ACCOUNT_FILE = 'service_account.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

def get_doc_id_by_title(meeting_title):
    query = f"name contains '{meeting_title}' and mimeType='application/vnd.google-apps.document'"
    results = drive_service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=1
    ).execute()

    items = results.get('files', [])
    if not items:
        return None
    return items[0]['id']

def get_doc_content(doc_id):
    document = docs_service.documents().get(documentId=doc_id).execute()
    content = document.get('body', {}).get('content', [])

    text = ""
    for value in content:
        if 'paragraph' in value:
            elements = value['paragraph'].get('elements', [])
            for elem in elements:
                if 'textRun' in elem:
                    text += elem['textRun'].get('content', '')
    return text

if __name__ == "__main__":
    title = "Sample Meeting"
    doc_id = get_doc_id_by_title(title)
    if doc_id:
        print("Doc ID:", doc_id)
        print(get_doc_content(doc_id))
