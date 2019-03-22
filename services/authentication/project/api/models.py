import unicodedata

from passlib.apps import custom_app_context as pwd_context
from random import SystemRandom

from project import db


class Password(db.Model):
    __tablename__ = 'passwords'

    user_id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    auth_allowed = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, user_id, password):
        self.password_hash = user_id
        self.set_password(password)

    def set_password(self, password):
        random_val = str(SystemRandom().getrandbits(32*8))  # generate a salt with 32 random bytes
        random_str = ""
        # Python chr(i) supports input from 0 to 1114111, so at least 6 digits/char allowed
        for i in range(0, len(random_val), 6):
            char_nr = int("".join(random_val[i + k] for k in range(6) if i + k < len(random_val)))
            char = chr(char_nr + 32)
            if unicodedata.category(char) not in 'cC':  # not a control character
                random_str += char
        self.salt = random_str
        self.password_hash = pwd_context.hash(self.salt + password)

    def verify_password(self, password):
        return pwd_context.verify(self.salt + password, self.password_hash)

    def to_json(self):
        return {
            'user_id': self.user_id,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'auth_allowed': self.auth_allowed
        }
