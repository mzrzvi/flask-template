"""
Facebook auth module
"""
from flask_oauth import OAuth

from app_name import app

oauth = OAuth()
oauth_settings = {
    'name': 'facebook',
    'base_url': 'https://graph.facebook.com/',
    'request_token_url': None,
    'access_token_url': '/oauth/access_token',
    'authorize_url': 'https://www.facebook.com/dialog/oauth',
    'consumer_key': app.config.get('FACEBOOK_APP_ID'),
    'consumer_secret': app.config.get('FACEBOOK_APP_SECRET'),
    'request_token_params': {
        'scope': 'email'
    }
}

fb_auth = oauth.remote_app(**oauth_settings)
