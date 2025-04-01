from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'service_account.json'  # place your credentials here
CALENDAR_ID = 'primary'  # or your specific calendar ID

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=creds)

def get_latest_past_meeting():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMax=now,
        singleEvents=True,
        orderBy='startTime',
        maxResults=10
    ).execute()

    events = events_result.get('items', [])
    past_events = [e for e in events if 'attendees' in e and e['start']['dateTime'] < now]
    if not past_events:
        return None

    return past_events[-1]  # Most recent past event

if __name__ == '__main__':
    event = get_latest_past_meeting()
    if event:
        print("Latest Meeting:", event['summary'], event['start']['dateTime'])
