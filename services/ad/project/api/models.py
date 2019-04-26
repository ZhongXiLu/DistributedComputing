
from project import db


class Ad(db.Model):
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(128), nullable=False)   # path to image file on local filesystem
    category = db.Column(db.String(128), nullable=False)

    def __init__(self, image, category):
        self.image = image
        self.category = category

    def to_json(self):
        return {
            'id': self.id,
            'image': self.image,
            'category': self.category
        }


class UserCategory(db.Model):
    __tablename__ = 'user_categories'

    user_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(128), nullable=False, primary_key=True)

    def __init__(self, user_id, category):
        self.user_id = user_id
        self.category = category

    def to_json(self):
        return {
            'user_id': self.user_id,
            'category': self.category
        }
