from flask import request
from flask_restplus import Api, Resource, abort, marshal

from . import API
from .api_models import BEVERAGE_GET
from .api_models import BEVERAGE_POST
from .api_models import BEVERAGE_PUT

from .. import DB
from ..db_models.beverage import Beverage

BEVERAGE_NS = API.namespace('beverages', description='Beverages', path='/beverages')

@BEVERAGE_NS.route('/')
class BeverageList(Resource):
    """
    List of all Beverages
    """

    #@jwt_required
    #@API.param('active', 'get only active lendings', type=bool, required=False, default=True)
    @API.marshal_list_with(BEVERAGE_GET)
    # pylint: disable=R0201
    def get(self):
        """
        Get a list of all beverages currently in the system
        """
        return Beverage.query.all()

    #@jwt_required
    #@satisfies_role(UserRole.ADMIN)
    @BEVERAGE_NS.doc(model=BEVERAGE_GET, body=BEVERAGE_POST)
    @BEVERAGE_NS.response(404, 'Requested item tag not found!')
    # pylint: disable=R0201
    def post(self):
        """
        Add a new beverage to the database
        """
        new = Beverage(**request.get_json())
        DB.session.add(new)
        DB.session.commit()
        return marshal(new, BEVERAGE_GET), 201

@BEVERAGE_NS.route('/<int:beverage_id>/')
class UserDetail(Resource):
    """
    A single beverage
    """

    #@jwt_required
    @API.marshal_with(BEVERAGE_GET)
    # pylint: disable=R0201
    def get(self, beverage_id):
        """
        Get the details of a single user
        """
        return Beverage.query.filter(Beverage.id == beverage_id).first()

   #@jwt_required
    #@satisfies_role(UserRole.ADMIN)
    @BEVERAGE_NS.doc(model=BEVERAGE_GET, body=BEVERAGE_PUT)
    @BEVERAGE_NS.response(404, 'Requested item tag not found!')
    # pylint: disable=R0201
    def put(self, beverage_id):
        """
        Update a single user
        """
        beverage = Beverage.query.filter(Beverage.id == beverage_id).first()

        if beverage is None:
            abort(404, 'Requested beverage not found!')

        beverage.update(**request.get_json())
        DB.session.commit()
        return marshal(beverage, BEVERAGE_GET), 200