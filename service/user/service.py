from models import UserInfo
from schemas import UserInfoDTO
from user.crud import user_info_crud


def get_user_info(user_id: int) -> UserInfoDTO:
    user_info = user_info_crud.read(user_id)
    return UserInfoDTO(first_name=user_info.first_name,
                       last_name=user_info.last_name)


def update_user_info(user_id: int, updated_user_info_dto: UserInfoDTO) -> UserInfoDTO:
    user_info = user_info_crud.read(user_id)
    user_info_to_update = UserInfo(id=user_info.id,
                                   user_id=user_info.user_id,
                                   first_name=updated_user_info_dto.first_name,
                                   last_name=updated_user_info_dto.last_name)
    updated_user_info = user_info_crud.update(user_info_to_update)
    return UserInfoDTO(first_name=updated_user_info.first_name,
                       last_name=updated_user_info.last_name)
