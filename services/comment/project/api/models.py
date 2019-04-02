
from sqlalchemy.sql import func

from project import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(4096), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, post_id, creator, content):
        self.post_id = post_id
        self.creator = creator
        self.content = content

    def to_json(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'creator': self.creator,
            'content': self.content,
            'created_date': self.created_date
        }
