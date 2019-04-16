

from project import db


class BadWord(db.Model):
    __tablename__ = 'badwords'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(1028), nullable=False)

    def __init__(self, word):
        self.word = word

    def to_json(self):
        return {
            'id': self.id,
            'word': self.word
        }
