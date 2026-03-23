import os
import requests
from urllib.parse import urlencode

CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:3000/callback'


def get_auth_url():
    """Generate LinkedIn authentication URL"""
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email w_member_social'
    }
    return f'https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}'


def get_access_token(code):
    """Exchange authorization code for access token"""
    url = 'https://www.linkedin.com/oauth/v2/accessToken'
    
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()['access_token']


def get_profile(access_token):
    """Get user profile information"""
    url = 'https://api.linkedin.com/v2/userinfo'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()


def create_post(access_token, text):
    """Create a post on LinkedIn"""
    # Get user profile to get the author ID
    profile = get_profile(access_token)
    author_id = profile['sub']
    
    url = 'https://api.linkedin.com/v2/ugcPosts'
    
    payload = {
        'author': f'urn:li:person:{author_id}',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': text
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
        }
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()
