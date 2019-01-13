"""
Module containing database models for everything concerning Transaction entries.
"""

from sqlalchemy.sql import func
from typing import List


from .. import DB
from . import STD_STRING_SIZE
from .user import User

__all__ = [ 'Transaction', ]


class Transaction(DB.Model):
    """
    The representation of a Transaction Entry
    """

    __tablename__ = 'Transaction'

    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey(User.id), nullable=True)
    amount = DB.Column(DB.Integer, nullable=True)
    reason = DB.Column(DB.Text, nullable=True)
    cancels_id = DB.Column(DB.Integer, DB.ForeignKey(id), nullable=True)
    timestamp = DB.Column(DB.DateTime, server_default=func.now())

    user = DB.relationship(User, lazy='joined')
    cancels = DB.relationship('Transaction', single_parent=True, uselist=False, lazy='joined')

    def __init__(self, user: User, amount: int, reason: str, cancels: 'Transaction' = None):
        self.user = user
        self.amount = amount
        self.reason = reason
        self.cancels = cancels


