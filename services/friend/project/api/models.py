
from project import db


class Friend(db.Model):
    __tablename__ = 'friends'

    friend_initiator_id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend_acceptor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_accepted = db.Column(db.Boolean, nullable=False)

    def __init__(self, friend_initiator_id, friend_acceptor_id):
        self.friend_initiator_id = friend_initiator_id
        self.friend_acceptor_id = friend_acceptor_id
        self.is_accepted = False

    def to_json(self):
        return {
            'friend_initiator_id': self.friend_initiator_id,
            'friend_acceptor_id': self.friend_acceptor_id,
            'is_accepted': self.is_accepted
        }
