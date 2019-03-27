

from project import db


class Tag(db.Model):
    __tablename__ = 'tags'

    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def to_json(self):
        return {
            'post_id': self.post_id,
            'user_id': self.user_id
        }
