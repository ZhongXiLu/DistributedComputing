from sqlalchemy import func

from project import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contents = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    time_sent = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, contents: str, sender_id: int, receiver_id: int):
        self.contents = contents
        self.sender_id = sender_id
        self.receiver_id = receiver_id

    def to_json(self):
        return {
            'id': self.id,
            'contents': self.contents,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'is_read': self.is_read,
            'time_sent': self.time_sent
        }
