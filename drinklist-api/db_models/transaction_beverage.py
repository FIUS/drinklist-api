"""
Module containing database models for everything concerning TransactionBeverage entries.
"""
from sqlalchemy.sql import func

from .. import DB
from . import STD_STRING_SIZE
from .beverage import Beverage
from .user import User
from .transaction import Transaction

__all__ = [ 'TransactionBeverage', ]

class TransactionBeverage(DB.Model):
    """
    The representation of a TransactionBeverage Entry
    """

    __tablename__ = 'TransactionBeverage'

    transaction_id = DB.Column(DB.Integer, DB.ForeignKey(Transaction.id), primary_key=True)
    beverage_id = DB.Column(DB.Integer, DB.ForeignKey(Beverage.id), primary_key=True)
    count = DB.Column(DB.Integer)
    price = DB.Column(DB.Integer)

    transaction = DB.relationship(Transaction, lazy='select', backref=DB.backref('beverages', lazy='joined'))
    beverage = DB.relationship(Beverage, lazy='joined')

    def __init__(self, transaction: Transaction, beverage: Beverage, count: int, price: int):
        self.transaction = transaction
        self.beverage = beverage
        self.count = count
        self.price = price
