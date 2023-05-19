from user.crud import user_crud
from models import UserInfo
from schemas import UserInfoDTO, UserVerboseInfoDTO
from user_info.crud import user_info_crud
from user_info.errors import UserNotExistingError
from user_info.utils import convert_user_to_dto, convert_user_info_to_dto


def get_user_verbose_info_by_id(user_id: int) -> UserVerboseInfoDTO:
    user = user_crud.read_by_id(user_id)
    if not user:
        raise UserNotExistingError(username)
    user_info = user_info_crud.read(user.id)
    return UserVerboseInfoDTO(user=convert_user_to_dto(user),
                              user_info=convert_user_info_to_dto(user_info))

def get_user_verbose_info_by_username(username: str) -> UserVerboseInfoDTO:
    user = user_crud.read(username)
    if not user:
        raise UserNotExistingError(username)
    user_info = user_info_crud.read(user.id)
    return UserVerboseInfoDTO(user=convert_user_to_dto(user),
                              user_info=convert_user_info_to_dto(user_info))


def update_user_info(user_id: int, updated_user_info_dto: UserInfoDTO) -> UserInfoDTO:
    user_info = user_info_crud.read(user_id)
    user_info_to_update = UserInfo(id=user_info.id,
                                   user_id=user_info.user_id,
                                   first_name=updated_user_info_dto.first_name,
                                   last_name=updated_user_info_dto.last_name)
    updated_user_info = user_info_crud.update(user_info_to_update)
    return convert_user_info_to_dto(updated_user_info)
