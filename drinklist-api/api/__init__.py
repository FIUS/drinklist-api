"""
Main API Module
"""
from typing import List
from functools import wraps
from flask import Blueprint
from flask_restplus import Api, Resource, abort, marshal
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_claims, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError, InvalidTokenError

from .. import APP, JWT, AUTH_LOGGER
from ..login import AuthUser, UserRole

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

def satisfies_role(role: UserRole, user_self_allowed: bool = False):
    """
    Check if the requesting user has one of the given roles.

    Must be applied after jwt_required decorator!
    """
    def has_roles_decorator(func):
        """
        Decorator function
        """
        @wraps(func)
        # pylint: disable=R1710
        def wrapper(*args, **kwargs):
            """
            Wrapper function
            """
            role_claims = get_jwt_claims()
            if user_self_allowed:
                name = get_jwt_identity()
                if name is not None and kwargs['user_name'] == name:
                    return func(*args, **kwargs)

            if role > role_claims:
                if user_self_allowed:
                    AUTH_LOGGER.debug('Access to ressource with isufficient rights. User %s with role %s wants to'
                                      'access data of user %s and would require role %s',
                                      name, UserRole(role_claims), kwargs['user_name'], role)
                AUTH_LOGGER.debug('Access to ressource with isufficient rights. User role: %s, required role: %s',
                                  UserRole(role_claims), role)
                abort(403, 'Only users with {} privileges have access to this resource.'.format(role.name))
            else:
                return func(*args, **kwargs)
        return wrapper
    return has_roles_decorator


API_BLUEPRINT = Blueprint('api', __name__)

def render_root(self):
    return self.make_response(marshal({}, ROOT_MODEL), 200)

Api.render_root = render_root

API = Api(API_BLUEPRINT, version='0.1', title='TTF API', doc='/doc/',
          authorizations=AUTHORIZATIONS, security='jwt',
          description='API for TTF.')

# pylint: disable=C0413
from .api_models import ROOT_MODEL, TRANSACTION_GET

@JWT.user_identity_loader
def load_user_identity(user: AuthUser):
    """
    Loader for the user identity
    """
    return user.name


@JWT.user_claims_loader
def load_user_claims(user: AuthUser):
    """
    Loader for the user claims
    """
    return user.role.value

@JWT.claims_verification_loader
def verify_claims(claims):
    return True

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
    AUTH_LOGGER.debug('Unauthorized access: %s', message)


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

from . import user, beverage, authentication, transaction

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

