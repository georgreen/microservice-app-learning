import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS


def create_app(config=None):
    # instantiate the app
    app = Flask(__name__)

    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    from project.api.models import db
    db.init_app(app)
    if app.config['DEBUG_TB_ENABLED']:
        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)

    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
