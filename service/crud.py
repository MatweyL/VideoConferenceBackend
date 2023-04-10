from abc import abstractmethod
from typing import Union, Iterable

from service.database import AbstractDB
from service.exceptions import PrimaryKeyAlreadyExistsError, UsernameAlreadyExistsError, UserNotExistingError
from service.models import User


class AbstractCRUD:

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def read(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, entity, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


class UserCRUD(AbstractCRUD):

    def __init__(self):
        self._users = {}

    def create(self, user: User) -> User:
        try:
            if user.username in self._users:
                raise BaseException
            self._users[user.username] = user
            return self._users[user.username]
        except BaseException:
            raise UsernameAlreadyExistsError(user.username)

    def read(self, username: str, *args, **kwargs) -> User:
        try:
            return self._users[username]
        except KeyError:
            raise UserNotExistingError(username)

    def update(self, user: User, *args, **kwargs) -> User:
        try:
            self._users[user.username] = user
            return self._users[user.username]
        except KeyError:
            raise UserNotExistingError(user.username)

    def delete(self, username: str, *args, **kwargs) -> User:
        try:
            return self._users.pop(username)
        except KeyError:
            raise UserNotExistingError(username)
