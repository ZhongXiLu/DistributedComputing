import unicodedata

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from random import SystemRandom

from project import db


def get_app():  # Avoid circular dependency
    if not hasattr(get_app, "app"):
        from project import create_app
        get_app.app = create_app()
    return get_app.app


class Password(db.Model):
    __tablename__ = 'passwords'

    user_id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    auth_allowed = db.Column(db.Boolean(), default=True, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, user_id, password, is_admin=False):
        self.user_id = user_id
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        random_val = str(SystemRandom().getrandbits(32*8))  # generate a salt with 32 random bytes
        # random_str = ""
        # # Python chr(i) supports input from 0 to 1114111, so at least 6 digits/char allowed
        # for i in range(0, len(random_val), 6):
        #     char_nr = int("".join(random_val[i + k] for k in range(6) if i + k < len(random_val)))
        #     char = chr(char_nr + 32)
        #     if unicodedata.category(char) not in 'cC':  # not a control character
        #         random_str += char
        # self.salt = random_str
        self.salt = random_val
        self.password_hash = pwd_context.hash(self.salt + password)

    def verify_password(self, password):
        return pwd_context.verify(self.salt + password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(get_app().config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'user_id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(get_app().config['SECRET_KEY'])
        try:

            data = s.loads(token)
        except SignatureExpired:
            return None  # Expired valid token
        except BadSignature:
            return None  # Invalid token
        user_id = Password.query.get(data['user_id'])
        return user_id

    def to_json(self):
        return {
            'user_id': self.user_id,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'auth_allowed': self.auth_allowed
        }
