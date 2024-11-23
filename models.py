from datetime import datetime, timezone
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class IPAddres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(46), nullable=False, unique=True)
    blacklist = db.Column(db.Boolean, default=False)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    