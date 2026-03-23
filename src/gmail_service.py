import os
import pickle
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_httplib2 import AuthorizedHttp
import googleapiclient.discovery
import base64
from email.mime.text import MIMEText

# Gmail API configuration
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

REDIRECT_URI = 'http://localhost:3000/google/callback'
TOKEN_FILE = 'token.pickle'

# Global OAuth2 client
oauth2_client = None


def get_oauth2_client():
    """Initialize and return OAuth2 client"""
    global oauth2_client
    
    if oauth2_client is None:
        oauth2_client = {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': REDIRECT_URI
        }
    
    return oauth2_client


def get_auth_url():
    """Generate Google authentication URL"""
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return auth_url


def set_tokens(code):
    """Exchange authorization code for tokens"""
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Save credentials for later use
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(credentials, token)
    
    return {
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_expiry': credentials.expiry.isoformat() if credentials.expiry else None
    }


def get_credentials():
    """Get valid credentials (load from file or refresh)"""
    credentials = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
    
    # Refresh credentials if expired
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    
    return credentials


def list_emails():
    """Get list of emails"""
    credentials = get_credentials()
    if not credentials:
        raise Exception('Google credentials not found. Please authenticate first.')
    
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    
    messages = results.get('messages', [])
    return messages


def send_email(email_data):
    """Send an email"""
    credentials = get_credentials()
    if not credentials:
        raise Exception('Google credentials not found. Please authenticate first.')
    
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)
    
    to = email_data['to']
    subject = email_data['subject']
    body = email_data['body']
    
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    service.users().messages().send(
        userId='me',
        body={'raw': raw_message}
    ).execute()
