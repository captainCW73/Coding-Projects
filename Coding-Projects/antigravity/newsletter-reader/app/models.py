from datetime import datetime
from . import db

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String, unique=True, nullable=False)
    source = db.Column(db.String, nullable=False)  # "apple_mail" or "gmail"
    sender_email = db.Column(db.String, nullable=False)
    sender_name = db.Column(db.String)
    subject = db.Column(db.String)
    date_received = db.Column(db.DateTime, nullable=False)
    body_html = db.Column(db.Text)
    body_text = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    is_newsletter = db.Column(db.Boolean, default=None, nullable=True) # None = unclassified
    synced_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Email {self.subject} from {self.sender_name}>'

class Sender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    is_newsletter = db.Column(db.Boolean) # AI-classified or user-confirmed
    confidence = db.Column(db.Float) # Gemini's confidence score (0-1)
    email_count = db.Column(db.Integer, default=0)
    user_override = db.Column(db.Boolean, nullable=True) # True if user manually set

    def __repr__(self):
        return f'<Sender {self.name} ({self.email})>'

class SyncLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String, nullable=False) # "apple_mail" or "gmail"
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    emails_synced = db.Column(db.Integer, default=0)
    status = db.Column(db.String, default='in_progress') # "success", "error", "in_progress"
    error_message = db.Column(db.Text)

    def __repr__(self):
        return f'<SyncLog {self.source} {self.status} at {self.started_at}>
'