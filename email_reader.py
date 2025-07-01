# email_reader.py
import os
import base64
import pickle
import datetime
from email import message_from_bytes
from typing import List

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Scopes - readonly access to Gmail
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_PATH = "token.pickle"

def authenticate_gmail():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service

def extract_body(email_msg) -> str:
    if email_msg.is_multipart():
        for part in email_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                continue

            if content_type == "text/plain":
                return part.get_payload(decode=True).decode(errors='ignore')

            elif content_type == "text/html":
                html = part.get_payload(decode=True).decode(errors='ignore')
                return html
    else:
        return email_msg.get_payload(decode=True).decode(errors='ignore')

    return "(No content)"

def get_latest_emails(limit: int = 5) -> List[dict]:
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', maxResults=limit, labelIds=["INBOX"]).execute()
    messages = results.get('messages', [])

    email_data = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        raw = base64.urlsafe_b64decode(msg_data['raw'].encode('ASCII'))
        email_msg = message_from_bytes(raw)

        subject = email_msg['subject']
        sender = email_msg['from']
        date = email_msg['date']
        body = extract_body(email_msg)

        email_data.append({
            "subject": subject,
            "from": sender,
            "date": date,
            "body": body
        })

    return email_data

def create_ics_file(title, description, start_time, filename="meeting.ics"):
    from ics import Calendar, Event
    calendar = Calendar()
    event = Event()
    event.name = title
    event.begin = start_time
    event.duration = datetime.timedelta(minutes=30)
    event.description = description
    calendar.events.add(event)

    with open(filename, "w") as f:
        f.writelines(calendar)

    return filename

if __name__ == "__main__":
    emails = get_latest_emails(3)
    for i, mail in enumerate(emails, 1):
        print(f"\n--- Email {i} ---")
        print("Subject:", mail['subject'])
        print("From:", mail['from'])
        print("Date:", mail['date'])
        print("Body:\n", mail['body'][:500])

        if "meeting" in mail['body'].lower():
            print("\n📅 Meeting detected. Creating calendar invite...")
            # Dummy date/time for now; ideally you'd extract it from email body with NLP
            create_ics_file(
                title=mail['subject'],
                description=mail['body'][:100],
                start_time="2025-06-26 15:00:00"  # This should be dynamically parsed
            )
            print("✅ Calendar file 'meeting.ics' created.")
