# -*- encoding: utf-8 -*-

import os
from decouple import config


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='mysql+pymysql'),
        config('DB_USERNAME', default='grupo2'),
        config('DB_PASS', default='ZTZlYzAyNmE3M2E1'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=3306),
        config('DB_NAME', default='grupo2')
    )

    GOOGLE_CLIENT_ID = config(
        'GOOGLE_CLIENT_ID', default='1010614499004-o5rhnk0lq8l62jv057bqflf3nstknvj7.apps.googleusercontent.com')
    GOOGLE_CLIENT_SECRET = config(
        'GOOGLE_CLIENT_SECRET', default='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')


class DebugConfig(Config):
    DEBUG = False


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
