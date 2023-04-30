from abc import abstractmethod
from typing import Dict

from core import SingletonMeta
from dto import UserCredentialsDTO
from exceptions import UsernameAlreadyExistsError, UserNotExistingError
from models import User


class AbstractCRUD:

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def read(self, pk, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, entity, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, pk, *args, **kwargs):
        pass


class CRUDManager(metaclass=SingletonMeta):

    def __init__(self):
        self._cruds: Dict = {
            User: UserCRUD()
        }

    def crud(self, crud_class) -> AbstractCRUD:
        return self._cruds[crud_class]


class UserCRUD(AbstractCRUD):

    def __init__(self):
        self._users = {}

    def create(self, user: UserCredentialsDTO) -> User:
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

    def update(self, user: UserCredentialsDTO, *args, **kwargs) -> User:
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


crud_manager = CRUDManager()
