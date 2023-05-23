from models import User, UserInfo
from schemas import UserDTO, UserInfoDTO


def convert_user_to_dto(user: User) -> UserDTO:
    return UserDTO(username=user.username, id=user.id)


def convert_user_info_to_dto(user_info: UserInfo) -> UserInfoDTO:
    return UserInfoDTO(first_name=user_info.first_name,
                       last_name=user_info.last_name)

