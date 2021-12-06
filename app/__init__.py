# -*- encoding: utf-8 -*-
from wtforms.validators import ValidationError
from app.views import blueprint
import os
from flask import Flask, url_for, Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from flask_migrate import Migrate
from config import config_dict
from decouple import config
from app.helpers import handler
from dotenv import load_dotenv
from flask_cors import CORS
from oauthlib.oauth2 import WebApplicationClient


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


def get_config(config_dict):
    # The configuration
    get_config_mode = 'Debug' if os.environ["FLASK_ENV"] != "production" else 'Production'

    try:

        # Load the configuration using the default values
        return config_dict[get_config_mode.capitalize()]
    except KeyError:
        exit(
            'Error: Invalid <config_mode>. Expected values [Debug, Production] ')


app_config = get_config(config_dict)

# OAuth 2 client setup
client = WebApplicationClient(app_config.GOOGLE_CLIENT_ID)


def register_cors(app):
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_errors(app):
    app.register_error_handler(500, handler.server_error)
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(403, handler.forbidden_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(400, handler.bad_request)


def register_blueprints(app):

    def register_directory(a: str, b: str):
        dir = (a, b)
        # https://stackoverflow.com/a/11969014/5739532
        files = [f for f in os.listdir(
            dir[0]) if os.path.isfile(os.path.join(dir[0], f))]
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file = os.path.splitext(file)[0]
                module = import_module(dir[1]+file)
                app.register_blueprint(module.blueprint)

    register_directory(a='./app/views', b='app.views.')
    register_directory(a='./app/views/api', b='app.views.api.')


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        drop_rec = os.getenv('DROP_RECREATE')
        if drop_rec and drop_rec.lower() == "true":
            from .populate_db import init_defaults
            db.drop_all()
            db.create_all(app=create_app())
            init_defaults()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app():

    app_config = get_config(config_dict)

    app = Flask(__name__, static_folder='static')
    app.config.from_object(app_config)
    # if you want log sql statement you should uncomment the following line
    #app.config['SQLALCHEMY_ECHO'] = True
    register_cors(app)
    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    configure_database(app)
    db.init_app(app)
    migrate.init_app(app, db)

    if DEBUG:
        app.logger.info('DEBUG       = ' + str(DEBUG))
        #app.logger.info('Environment = ' + get_config_mode)
        app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

    return app
