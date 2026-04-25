import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    with app.app_context():
        from .routes import inbox, reader, api
        app.register_blueprint(inbox.bp)
        app.register_blueprint(reader.bp)
        app.register_blueprint(api.bp)

        db.create_all()

        # Auto-trigger newsletter detection if no senders exist yet
        from .models import Sender
        from .services.newsletter_detector import NewsletterDetector
        if Sender.query.first() is None:
            detector = NewsletterDetector(app)
            detector.detect_newsletters()

    return app
