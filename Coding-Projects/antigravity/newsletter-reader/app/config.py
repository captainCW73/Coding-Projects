import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/newsletters.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GMAIL_CREDENTIALS_PATH = 'credentials/credentials.json'
    GMAIL_TOKEN_PATH = 'credentials/token.json'
    INITIAL_SCAN_LIMIT = int(os.environ.get('INITIAL_SCAN_LIMIT', 500))
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_if_not_set') # IMPORTANT: Change this in .env
