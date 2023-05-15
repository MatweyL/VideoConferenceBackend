from fastapi import APIRouter, Depends, HTTPException

from user.service import get_user_by_jwt_token
from models import User
from schemas import UserDTO, UserInfoDTO, UserVerboseInfoDTO
from user_info.errors import UserNotExistingError
from user_info.service import update_user_info, get_user_verbose_info_by_username
from user_info.utils import convert_user_to_dto

router = APIRouter()


@router.get('/me', response_model=UserVerboseInfoDTO)
async def get_current_user_profile(user: User = Depends(get_user_by_jwt_token)):
    user_verbose_info = get_user_verbose_info_by_username(user.username)
    return user_verbose_info


@router.get('/', response_model=UserVerboseInfoDTO)
async def get_other_user_profile(username: str, user: User = Depends(get_user_by_jwt_token)):
    try:
        user_verbose_info = get_user_verbose_info_by_username(username)
    except UserNotExistingError as e:
        raise HTTPException(status_code=404, detail=str(e))
    else:
        return user_verbose_info


@router.put('/me')
async def update_profile(updated_user: UserInfoDTO, user: User = Depends(get_user_by_jwt_token)):
    user_info = update_user_info(user.id, updated_user)
    return UserVerboseInfoDTO(user=convert_user_to_dto(user),
                              user_info=user_info)
