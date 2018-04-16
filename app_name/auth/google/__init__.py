"""
Google auth module
"""

from app_name import app

from flask_dance.contrib.google import make_google_blueprint

blueprint = make_google_blueprint(
    client_id=app.config.get('GOOGLE_CLIENT_ID'),
    client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"]
)

app.register_blueprint(blueprint, url_prefix="/login")
