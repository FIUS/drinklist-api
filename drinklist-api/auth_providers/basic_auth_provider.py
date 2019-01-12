"""
Auth Provider which provides three simple hardcoded logins for debugging purposes.
"""

from typing import Dict, List
from ..login import LoginProvider
from .. import APP

class BasicAuthProvider(LoginProvider, provider_name="Basic"):
    """
    Example Login Provider with hardcoded insecure accounts.
    """

    ACCOUNTS: Dict[str, str] = APP.config['BASIC_AUTH_USERS']

    ADMINS: List[str] = APP.config['BASIC_AUTH_ADMINS']
    KIOSK: List[str] = APP.config['BASIC_AUTH_KIOSK']
    USER: List[str] = APP.config['BASIC_AUTH_USER']

    def __init__(self):
        pass

    def init(self) -> None:
        pass

    def valid_user(self, user_id: str) -> bool:
        print("RES" + user_id)
        return user_id in self.ACCOUNTS

    def valid_password(self, user_id: str, password: str) -> bool:
        return self.ACCOUNTS[user_id] == password

    def is_admin(self, user_id: str) -> bool:
        return user_id in self.ADMINS

    def is_kiosk_user(self, user_id: str) -> bool:
        return user_id in self.KIOSK

    def is_consuming_user(self, user_id: str) -> bool:
        return user_id in self.USER
