from auth.exceptions import UsernameAlreadyExistsError, UserNotExistingError
from auth.schemas import UserCredentialsDTO
from crud import AbstractCRUD
from database import get_session
from models import User


class UserInMemoryCRUD(AbstractCRUD):

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


class UserCRUD(AbstractCRUD):

    def __init__(self):
        self._users = {}

    def create(self, user: User) -> User:
        with get_session() as session:
            existed_user = session.query(User).filter(User.username == user.username).first()
            if existed_user:
                raise UsernameAlreadyExistsError(user.username)

            session.add(user)
            session.commit()
            return user

    def read(self, username: str, *args, **kwargs) -> User:
        try:
            with get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                if not user:
                    raise UserNotExistingError(username)
                else:
                    return user
        except BaseException:
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


user_crud = UserCRUD()
