from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# initialization
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# extensions
db = SQLAlchemy(app)
from api import api
from api import login