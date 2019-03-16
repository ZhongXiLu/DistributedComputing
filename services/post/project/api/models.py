

from sqlalchemy.sql import func

from project import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.Integer, nullable=False)     # user_id
    content = db.Column(db.String(4096), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, creator, content):
        self.creator = creator
        self.content = content

    def to_json(self):
        return {
            'id': self.id,
            'creator': self.creator,
            'content': self.content,
            'created_date': self.created_date
        }
