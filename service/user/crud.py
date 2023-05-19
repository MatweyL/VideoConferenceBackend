from .errors import UsernameAlreadyExistsError, UserNotExistingError
from crud import AbstractCRUD
from database import get_session
from models import User


class UserCRUD(AbstractCRUD):

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

    def read_by_id(self, user_id: int):
        try:
            with get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    raise UserNotExistingError(user_id)
                else:
                    return user
        except BaseException:
            raise UserNotExistingError(user_id)

    def update(self, updated_user: User, *args, **kwargs) -> User:
        try:
            with get_session() as session:
                session.add(updated_user)
                return updated_user
        except KeyError:
            raise UserNotExistingError(updated_user.username)

    def delete(self, username: str, *args, **kwargs) -> User:
        try:
            with get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                session.delete(user)
                return user
        except KeyError:
            raise UserNotExistingError(username)


user_crud = UserCRUD()
