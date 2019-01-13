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

    BASIC_AUTH_USERS = {}
    BASIC_AUTH_ADMIN = []
    BASIC_AUTH_KIOSK = []
    BASIC_AUTH_USER = []

    LDAP_URI = ""
    LDAP_PORT = 0
    LDAP_SSL = False
    LDAP_START_TLS = False
    LDAP_USER_SEARCH_BASE = ""
    LDAP_GROUP_SEARCH_BASE = ""
    LDAP_USER_RDN = ""
    LDAP_USER_UID_FIELD = ""
    LDAP_GROUP_MEMBERSHIP_FIELD = ""
    LDAP_CONSUMER_FILTER = ""
    LDAP_KIOSK_USER_FILTER = ""
    LDAP_ADMIN_FILTER = ""
    LDAP_CONSUMER_GROUP_FILTER = ""
    LDAP_KIOSK_USER_GROUP_FILTER = ""
    LDAP_ADMIN_GROUP_FILTER = ""

    LOGGING = {
        'version': 1,
        'formatters': {
            'extended': {
                'format': '%(asctime)s [%(levelname)s] [%(name)-16s] %(message)s <%(module)s, \
                %(funcName)s, %(lineno)s; %(pathname)s>',
            },
            'short': {
                'format': '[%(asctime)s] [%(levelname)s] [%(name)-16s] %(message)s',
            }
        },
        'handlers': {
            'default': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'extended',
                'filename': '/tmp/drinklist-api-default.log',
                'maxBytes': 104857600,
                'backupCount': 10,
            },
            'auth': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'short',
                'filename': '/tmp/drinklist-api-auth.log',
                'maxBytes': 104857600,
                'backupCount': 10,
            },
            'query': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'short',
                'filename': '/tmp/drinklist-api-querys.log',
                'maxBytes': 104857600,
                'backupCount': 2,
            },
            'console': {
                'class' : 'logging.StreamHandler',
                'formatter': 'extended',
            }
        },
        'loggers': {
            'flask.app.auth': {
                'level': logging.INFO,
                'propagate': False,
                'handlers': ['auth'],
            },
            'flask.app.db': {
                'level': logging.WARNING,
                'propagate': False,
                'handlers': ['query'],
            },
            'sqlalchemy': {
                'level': logging.WARNING,
                'propagate': False,
                'handlers': ['query'],
            },
        },
        'root': {
            'level': logging.WARNING,
            'handlers': ['default'],
        },
        'disable_existing_loggers': True,
    }

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

    BASIC_AUTH_ADMIN = ["admin"]
    BASIC_AUTH_KIOSK = ["kiosk"]
    BASIC_AUTH_USER = ["user1", "user2"]

    Config.LOGGING['loggers']['flask.app.auth']['level'] = logging.DEBUG
    Config.LOGGING['loggers']['flask.app.db']['level'] = logging.DEBUG
    Config.LOGGING['loggers']['sqlalchemy.engine'] = {
        'level': logging.WARN,
        'propagate': False,
        'handlers': ['query'],
    }
    Config.LOGGING['root']['handlers'].append('console')

class TestingConfig(Config):
    TESTING = True
