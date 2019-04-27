
from sqlalchemy.sql import func

from project import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(4096), nullable=False)
    recipient = db.Column(db.Integer, nullable=False)
    is_read = db.Column(db.Boolean(), default=False, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, content, recipient):
        self.content = content
        self.recipient = recipient

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'recipient': self.recipient,
            'is_read': self.is_read,
            'created_date': self.created_date
        }
