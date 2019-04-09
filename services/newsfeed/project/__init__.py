import os

from flask import Flask
from flask_cors import CORS


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from project.api.newsfeed import newsfeed_blueprint
    app.register_blueprint(newsfeed_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
