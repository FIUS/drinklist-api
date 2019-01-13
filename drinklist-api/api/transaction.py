from datetime import datetime
from flask import request
from flask_restplus import Api, Resource, abort, marshal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from . import API
from . import APP
from .api_models import TRANSACTION_GET
from .api_models import TRANSACTION_POST
from .api_models import TRANSACTION_DELETE

from .. import DB
from ..db_models.transaction import Transaction
from ..db_models.user import User
from ..db_models.transaction_beverage import TransactionBeverage
from ..db_models.beverage import Beverage

USER_NS = API.namespace('users', description='Users', path='/users')

@USER_NS.route('/<string:user_name>/transactions')
class TransactionList(Resource):
    """
    List of all Transactions
    """
   
    #@jwt_required
    #@API.param('active', 'get only active lendings', type=bool, required=False, default=True)
    @API.marshal_list_with(TRANSACTION_GET)
    @USER_NS.response(404, 'Requested User does not exist!')
    # pylint: disable=R0201
    def get(self, user_name: str):
        """
        Get a list of all transactions of the specified user currently in the system
        """
        user = User.query.filter(User.name == user_name).first()
        if user is None:
            abort(404, 'Requested User does not exist!')
        return Transaction.query.filter(Transaction.user_id == user_name).all()

    #@jwt_required
    #@satisfies_role(UserRole.ADMIN)
    @USER_NS.doc(model=TRANSACTION_GET, body=TRANSACTION_POST)
    @USER_NS.response(400, 'Specified beverage does not exist')
    @USER_NS.response(404, 'Specified User does not exist!')
    @USER_NS.response(409, 'Name is not unique!')
    @USER_NS.response(201, 'Created.')
    # pylint: disable=R0201
    def post(self, user_name: str):
        """
        Add a new transaction to the database
        """
        user = User.query.filter(User.name == user_name).first()
        if user is None:
            abort(404, 'Spezified User does not exist!')
        new_transaction = Transaction(user, request.get_json()['amount'], request.get_json()['reason'])
        beverages = request.get_json()['beverages']
        try:
            DB.session.add(new_transaction)
            for beverage in beverages:
                refered_beverage_id = beverage['beverage']['id']
                refered_beverage = Beverage.query.filter(Beverage.id == refered_beverage_id).first()
                if refered_beverage is None:
                    abort(400, 'Specified beverage does not exist')
                new_beverage = TransactionBeverage(new_transaction, refered_beverage, beverage['count'], beverage['price'])
                DB.session.add(new_beverage)
            DB.session.commit()
            return marshal(new_transaction, TRANSACTION_GET), 201
        except IntegrityError as err:
            message = str(err)
            if APP.config['DB_UNIQUE_CONSTRAIN_FAIL'] in message:
                abort(409, 'Name is not unique!')
            abort(500)


@USER_NS.route('/<string:user_name>/transactions/<int:transaction_id>')
class UserDetail(Resource):
    """
    A single transaction
    """

    #@jwt_required
    @API.marshal_with(TRANSACTION_GET)
    @USER_NS.response(404, 'Specified User does not exist!')
    # pylint: disable=R0201
    def get(self, transaction_id: int, user_name: str):
        """
        Get the details of a single transaction
        """
        #TODO check if the user is involved with that transaction otherwise 404
        user = User.query.filter(User.id == user_name).first()
        if user is None:
            abort(404, 'Specified User does not exist!')
        return Transaction.query.filter(Transaction.id == transaction_id).first()

    #@jwt_required
    #@satisfies_role(UserRole.ADMIN)
    @USER_NS.doc(model=TRANSACTION_GET, body=TRANSACTION_DELETE)
    @USER_NS.response(404, 'Specified User does not exist!')
    @USER_NS.response(409, 'Name is not unique!')
    @USER_NS.response(410, 'Reverse Deadline not met')
    @USER_NS.response(500, 'Something went wrong')
    # pylint: disable=R0201
    def delete(self, transaction_id: int, user_name: str):
        """
        Revert specified transaction in the database (adds a revertTransaction)
        """
        #TODO check if the user is involved with that transaction otherwise 404
        user = User.query.filter(User.id == user_name).first()
        if user is None:
            abort(404, 'Specified User does not exist!')
        reason = request.get_json()['reason']
        transaction = Transaction.query.filter(Transaction.id == transaction_id).first()
        #TODO timestamp bei >func.now()+5 min
        if False:
            print('hurra')
        #if transaction.timestamp > func.now()+ datetime.minute(5):
        #    abort(410, 'Reverse Deadline not met')
        else:
            reverse_transaction = Transaction(transaction.user, -transaction.amount, reason, transaction)
            beverages = transaction.beverages
            try:
                DB.session.add(reverse_transaction)
                for beverage in beverages:
                    reversed_beverage = TransactionBeverage(reverse_transaction, beverage.beverage, -(beverage.count), beverage.price)
                    DB.session.add(reversed_beverage)
                DB.session.commit()
                return marshal(reverse_transaction, TRANSACTION_GET), 201
            except IntegrityError as err:
                message = str(err)
                if APP.config['DB_UNIQUE_CONSTRAIN_FAIL'] in message:
                    abort(409, 'Name is not unique!')
                abort(500)
