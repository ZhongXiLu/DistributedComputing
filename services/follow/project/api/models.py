
from project import db


class Follower(db.Model):
    __tablename__ = 'follow'

    follower_id = db.Column(db.Integer, primary_key=True, nullable=False)
    followee_id = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, follower_id, followee_id):
        self.follower_id = follower_id
        self.followee_id = followee_id

    def to_json(self):
        return {
            'follower_id': self.follower_id,
            'followee_id': self.followee_id
        }
