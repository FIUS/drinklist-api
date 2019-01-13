from flask import request
from flask_restplus import Api, Resource, abort, marshal

from sqlalchemy.exc import IntegrityError

from . import API
from .api_models import USER_GET, USER_PUT

from .. import DB
from ..db_models.user import User


USER_NS = API.namespace('users', description='Users', path='/users')

@USER_NS.route('/')
class UserList(Resource):
    """
    The list of all Users
    """

    #@jwt_required
    #@satisfies_role(UserRole.ADMIN)
    @API.marshal_list_with(USER_GET)
    # pylint: disable=R0201
    def get(self):
        """
        Get a list of all users currently in the system
        """
        return User.query.all()

@USER_NS.route('/<string:user_name>/')
class UserDetail(Resource):
    """
    A single user
    """

    #@jwt_required
    @API.marshal_with(USER_GET)
    @USER_NS.response(404, 'Specified User does not exist!')
    # pylint: disable=R0201
    def get(self, user_name: str):
        """
        Get the details of a single user
        """
        user = User.query.filter(User.name == user_name).first()
        if user is None:
            abort(404, 'Specified User does not exist!')
        return user
        
    #@jwt_required
    #@satisfies_role(UserRole.ADMIN)
    @USER_NS.doc(model=USER_GET, body=USER_PUT)
    @USER_NS.response(404, 'Specified User does not exist!')
    # pylint: disable=R0201
    def put(self, user_name: str):
        """
        Update a single user
        """
        user = User.query.filter(User.name == user_name).first()

        if user is None:
            abort(404, 'Specified User does not exist!')

        user.update(**request.get_json())
        DB.session.commit()
        return marshal(user, USER_GET), 200