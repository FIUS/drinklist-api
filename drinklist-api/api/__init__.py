"""
Main API Module
"""
from typing import List
from flask import Blueprint
from flask_restplus import Api, Resource, abort, marshal
from flask_jwt_extended import jwt_required, jwt_optional
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError, InvalidTokenError

from .. import APP, JWT

from ..db_models.transaction import Transaction

AUTHORIZATIONS = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Standard JWT access token.'
    },
    'jwt-refresh': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT refresh token.'
    }
}


API_BLUEPRINT = Blueprint('api', __name__)

def render_root(self):
    return self.make_response(marshal({}, ROOT_MODEL), 200)

Api.render_root = render_root

API = Api(API_BLUEPRINT, version='0.1', title='TTF API', doc='/doc/',
          authorizations=AUTHORIZATIONS, security='jwt',
          description='API for TTF.')

# pylint: disable=C0413
from .api_models import ROOT_MODEL, TRANSACTION_GET

from . import user, beverage

@JWT.expired_token_loader
@API.errorhandler(ExpiredSignatureError)
def expired_token():
    """
    Handler function for a expired token
    """
    message = 'Token is expired.'
    log_unauthorized(message)
    abort(401, message)


@JWT.invalid_token_loader
@API.errorhandler(InvalidTokenError)
def invalid_token(message: str):
    """
    Handler function for a invalid token
    """
    log_unauthorized(message)
    abort(401, message)


@JWT.unauthorized_loader
def unauthorized(message: str):
    """
    Handler function for a unauthorized api access
    """
    log_unauthorized(message)
    abort(401, message)


@JWT.needs_fresh_token_loader
def stale_token():
    """
    Handler function for a no more fresh token
    """
    message = 'The JWT Token is not fresh. Please request a new Token directly with the /auth resource.'
    log_unauthorized(message)
    abort(403, message)


@JWT.revoked_token_loader
def revoked_token():
    """
    Handler function for a revoked or invalid token
    """
    message = 'The Token has been revoked.'
    log_unauthorized(message)
    abort(401, message)


@API.errorhandler(NoAuthorizationError)
def missing_header(error):
    """
    Handler function for a NoAuthorizationError
    """
    log_unauthorized(error.message)
    return {'message': error.message}, 401


@API.errorhandler
def default_errorhandler(error):
    """
    Handler function for a logging all errors
    """
    #APP.logger.exception()
    return {'message': error.message}, 500


def log_unauthorized(message):
    """
    Logs unauthorized access
    """
    pass  #AUTH_LOGGER.debug('Unauthorized access: %s', message)


APP.register_blueprint(API_BLUEPRINT, url_prefix='')

ROOT_NS = API.namespace('default', path='/')

@ROOT_NS.route('/')
class RootResource(Resource):
    """
    The API root element
    """

    @API.doc(security=None)
    @jwt_optional
    @API.marshal_with(ROOT_MODEL)
    # pylint: disable=R0201
    def get(self):
        """
        Get the root element
        """
        print('HI')
        return None

API.render_root = RootResource.get

HISTORY_NS = API.namespace('history', description='History', path='/history')

@HISTORY_NS.route('/')
class HistoryResource(Resource):
    """
    History
    """

    #@jwt_required
    @API.marshal_list_with(TRANSACTION_GET)
    # pylint: disable=R0201
    def get(self):
        """
        Get a list of all lendings currently in the system
        """
        return Transaction.query.all()

