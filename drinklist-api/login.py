"""
Module for the authentication and user handling
"""

from enum import IntEnum
from typing import Dict, List, Union
from abc import ABC, abstractmethod
from .db_models.user import User
from . import DB

class UserRole(IntEnum):
    """
    This Enum describes the possible rights / access levels to the software.
    """

    USER = 1
    KISOK_USER = 2
    ADMIN = 3

# pylint: disable=R0903
class AuthUser():
    """
    This Class represents a user in the system.
    """

    name: str
    role: UserRole = UserRole.USER
    _login_provider: Union['LoginProvider', None]

    def __init__(self, name: str, login_provider: Union['LoginProvider', None] = None):
        self.name = name
        self._login_provider = login_provider


class LoginProvider(ABC):
    """
    Abstract class which allows the login service to lookup users.
    """

    __registered_providers__: Dict[str, 'LoginProvider'] = {}

    def __init_subclass__(cls, provider_name: str = None):
        if provider_name is None:
            LoginProvider.register_provider(cls.__name__, cls())
        else:
            LoginProvider.register_provider(provider_name, cls())

    @staticmethod
    def register_provider(name: str, login_provider: 'LoginProvider'):
        """
        Register an Instance of LoginProvider under given name.

        Arguments:
            name {str} -- Name of the LoginProvider
            login_provider {LoginProvider} -- LoginProvider Instance

        Raises:
            KeyError -- If name is already registered with a different LoginProvider
        """
        if name in LoginProvider.__registered_providers__:
            raise KeyError('Name already in use!')
        LoginProvider.__registered_providers__[name] = login_provider

    @staticmethod
    def get_login_provider(name: str) -> Union['LoginProvider', None]:
        """
        Get a registered LoginProvider by its name.

        Arguments:
            name {str} -- Name of the LoginProvider

        Returns:
            Union[LoginProvider, None] -- LoginProvider or None
        """
        return LoginProvider.__registered_providers__.get(name)

    @staticmethod
    def list_login_providers() -> List[str]:
        """
        Get a list of Registered names of LoginProviders.

        Returns:
            List[str] -- All registered names of LoginProviders.
        """

        return list(LoginProvider.__registered_providers__.keys())

    @abstractmethod
    def init(self) -> None:
        """
        Init function which is called when the LoginProvider is connected to a
        LoginService.
        """
        pass

    @abstractmethod
    def valid_user(self, user_id: str) -> bool:
        """
        Check function to check if a user name exists or possibly exists
        """
        pass

    @abstractmethod
    def valid_password(self, user_id: str, password: str) -> bool:
        """
        Check function if a user id and password are valid
        """
        pass

    @abstractmethod
    def is_kiosk_user(self, user_id: str) -> bool:
        """
        Check function if a user can view all users pages
        """
        pass

    @abstractmethod
    def is_consuming_user(self, user_id: str) -> bool:
        """
        Check function if a user is actually using the drinklist
        """
        pass

    @abstractmethod
    def is_admin(self, user_id: str) -> bool:
        """
        Check function if a user has moderator privilages
        """
        pass


class LoginService():
    """
    This class handles the actual login with the help of a valid login provider.
    """

    _login_providers: List[LoginProvider]

    def __init__(self, login_providers: List[str]):
        self._login_providers = []

        if login_providers:
            for name in login_providers:
                provider = LoginProvider.get_login_provider(name)
                if provider:
                    provider.init()
                    self._login_providers.append(provider)

    def get_user(self, user: str, password: str) -> AuthUser:
        """
        Getter for a user object
        """
        for provider in self._login_providers:
            if provider.valid_user(user) and provider.valid_password(user, password):
                user_obj = AuthUser(user, provider)
                if provider.is_admin(user):
                    user_obj.role = UserRole.ADMIN
                elif provider.is_moderator(user):
                    user_obj.role = UserRole.MODERATOR
                elif provider.is_consuming_user(user):
                    db_user = User.query().filter(User.name == user)
                    if db_user is None:
                        db_user = User(user)
                        DB.session.add(db_user)
                        DB.session.commit()
                return user_obj
        return None

    def check_password(self, user: AuthUser, password: str) -> bool:
        """
        Check function for a password with an existing user object
        """

        provider = user._login_provider
        if provider:
            return provider.valid_password(user.name, password)

        return False
