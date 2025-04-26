from __future__ import print_function
import datetime
import os.path
from dateutil import parser

from google.auth.transport import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
credentials_path = '../credentials.json'
token_path = '../token.json'

def get_todays_events():
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no valid credentials, let the user log in'
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0,microsecond=0).isoformat() + 'Z'
    end_of_day = now.replace(hour=23, minute=59, second=59,microsecond=0).isoformat() + 'Z'

    # Call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=start_of_day, timeMax=end_of_day, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return []
    
    todays_events = []

    for event in events:
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')

        try:
            start_time = datetime.datetime.fromisoformat(start).strftime("%H:%M")
            end_time = datetime.datetime.fromisoformat(end).strftime("%H:%M")
            todays_events.append(f"{start_time} to {end_time} - {event.get('summary', 'No Title')}")
        except:
            todays_events.append(f"All day - {event.get('summary', 'No Title')}")


    return todays_events