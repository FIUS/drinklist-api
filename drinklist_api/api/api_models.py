"""
Module containing models for whole API to use.
"""

from flask_restplus import fields
from . import API
from ..db_models import STD_STRING_SIZE

ROOT_MODEL = API.model('RootModel', {
    'beverages': fields.Url('api.beverages_beverage_list'),
    'users': fields.Url('api.users_user_list'),
    'history': fields.Url('api.history_history_resource'),
    'authentication': fields.Url('api.auth_authentication_routes'),
})

AUTHENTICATION_ROUTES_MODEL = API.model('AuthenticationRoutesModel', {
    'login': fields.Url('api.auth_login'),
    'fresh_login': fields.Url('api.auth_fresh_login'),
    'refresh': fields.Url('api.auth_refresh'),
    'check': fields.Url('api.auth_check'),
})


BEVERAGE_POST = API.model('BeveragePOST', {
    'name': fields.String(max_length=STD_STRING_SIZE, title='Name'),
    'price': fields.Integer(title='Price'),
    'stock': fields.Integer(title='Stock'),
})

BEVERAGE_PUT = API.inherit('BeveragePUT', BEVERAGE_POST, {})

BEVERAGE_GET = API.inherit('BeverageGET', BEVERAGE_PUT, {
    'id': fields.Integer(min=1, example=1, title='Internal Identifier'),
})

USER_PUT = API.model('UserPUT', {
    'active': fields.Boolean(title='Active'),
})

USER_GET = API.inherit('UserGET', USER_PUT, {
    'name': fields.String(max_length=STD_STRING_SIZE, title='Name'),
    'id': fields.Integer(min=1, example=1, readonly=True, title='Internal Identifier'),
    'balance': fields.Integer(title='Balance'),
})

TRANSACTION_BEVERAGE_GET = API.model('TransactionBeverageGET', {
    'beverage': fields.Nested(BEVERAGE_GET),
    'count': fields.Integer(example=-1, title='Count of beverages'),
    'price': fields.Float(title='Price of beverage', readonly=True),
})

TRANSACTION_POST = API.model('TransactionPOST', {
    'beverages': fields.List(fields.Nested(TRANSACTION_BEVERAGE_GET)),
    'amount': fields.Integer(),
    'reason': fields.String(),
})

TRANSACTION_GET_NOCHILD = API.inherit('TransactionNoChildGET', TRANSACTION_POST, {
    'id': fields.Integer(),
    'timestamp': fields.DateTime(),
})

TRANSACTION_GET = API.inherit('TransactionGET', TRANSACTION_GET_NOCHILD, {
    'cancels': fields.Nested(TRANSACTION_GET_NOCHILD),
})

TRANSACTION_DELETE = API.model('TransactionDELETE', {
    'reason': fields.String(),
})
