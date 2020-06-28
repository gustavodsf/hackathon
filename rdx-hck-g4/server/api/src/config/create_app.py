# -*- coding: utf-8 -*-
"""Create flask instance."""

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from api.src.blueprints.voice.api import voice_blueprint
from api.src.blueprints.text.api  import text_blueprint
from api.src.blueprints.files.api  import files_blueprint
from api.src.blueprints.data.api  import data_blueprint

from os import path


def create_app():
    """Create a new flask app using the configuration files."""
    filePath = path.abspath(path.dirname(__file__))
    app = Flask("api", instance_path=filePath,
                instance_relative_config=True)
    app.config.from_object('api.src.config.default_settings')
    app.config.from_pyfile('config.cfg')
    app.register_blueprint(voice_blueprint)
    app.register_blueprint(text_blueprint)
    app.register_blueprint(files_blueprint)
    app.register_blueprint(data_blueprint)
    DebugToolbarExtension(app)
    CORS(app, supports_credentials=True)
    Swagger(app)
    return app
