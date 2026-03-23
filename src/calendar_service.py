import os
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
import googleapiclient.discovery
from gmail_service import get_credentials

TOKEN_FILE = 'token.pickle'


def get_calendar_service():
    """Get authenticated Google Calendar service"""
    credentials = get_credentials()
    if not credentials:
        raise Exception('Google credentials not found. Please authenticate first.')
    
    return googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)


def list_events():
    """List upcoming events from primary calendar"""
    service = get_calendar_service()
    
    now = datetime.utcnow().isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    return events


def create_event(summary, description, start, end):
    """Create a new event"""
    service = get_calendar_service()
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'Asia/Ho_Chi_Minh'
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Asia/Ho_Chi_Minh'
        }
    }
    
    created_event = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()
    
    return created_event
