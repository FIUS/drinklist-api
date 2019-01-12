"""Module containing default config values."""

from random import randint
import logging


class Config(object):
    DEBUG = False
    TESTING = False
    RESTPLUS_VALIDATE = True
    JWT_CLAIMS_IN_REFRESH_TOKEN = True
    JWT_SECRET_KEY = ''.join(hex(randint(0, 255))[2:] for i in range(16))
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_UNIQUE_CONSTRAIN_FAIL = 'UNIQUE constraint failed'

    LOGIN_PROVIDERS = ['Basic']

    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    RESTPLUS_JSON = {'indent': None}


class ProductionConfig(Config):
    pass


class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    JWT_SECRET_KEY = 'debug'

    BASIC_AUTH_USERS = {
        "admin": "admin",
        "kiosk": "kiosk",
        "user1": "user1",
        "user2": "user2",
    }

    BASIC_AUTH_ADMINS = ["admin"]
    BASIC_AUTH_KIOSK = ["kiosk"]
    BASIC_AUTH_USER = ["user"]

class TestingConfig(Config):
    TESTING = True
