from crud import AbstractCRUD
from database import get_session
from models import UserInfo
from user.exceptions import UserInfoNotExistingError


class UserInfoCRUD(AbstractCRUD):
    def create(self, user_info: UserInfo) -> UserInfo:
        with get_session() as session:
            session.add(user_info)
            session.commit()
            return user_info

    def read(self, user_id: int, *args, **kwargs) -> UserInfo:
        with get_session() as session:
            user_info = session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
            if not user_info:
                raise UserInfoNotExistingError()
            return user_info

    def update(self, updated_user_info: UserInfo, *args, **kwargs) -> UserInfo:
        with get_session() as session:
            session.add(updated_user_info)
            session.commit()
            return updated_user_info

    def delete(self, user_id: int, *args, **kwargs) -> UserInfo:
        with get_session() as session:
            user_info = session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
            session.delete(user_info)
            session.commit()
            return user_info


user_info_crud = UserInfoCRUD()
