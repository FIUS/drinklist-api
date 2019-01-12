from flask_restplus import Api, Resource, abort, marshal

from . import API
from .api_models import USER_GET

from ..db_models.user import User

USER_NS = API.namespace('users', description='Users', path='/users')

@USER_NS.route('/')
class UserList(Resource):
    """
    Users
    """

    #@jwt_required
    @API.marshal_list_with(USER_GET)
    # pylint: disable=R0201
    def get(self):
        """
        Get a list of all lendings currently in the system
        """
        return User.query.all()


