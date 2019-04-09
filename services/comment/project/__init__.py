import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# instantiate the db
db = SQLAlchemy()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.comment import comment_blueprint
    app.register_blueprint(comment_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
