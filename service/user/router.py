from fastapi import APIRouter, Depends

from auth.service import get_user_by_jwt_token
from models import User
from schemas import UserDTO, UserInfoDTO, UserVerboseInfoDTO
from user.service import get_user_info, update_user_info

router = APIRouter()


@router.get('/me')
async def get_profile(user: User = Depends(get_user_by_jwt_token)):
    user_info = get_user_info(user.id)
    return UserVerboseInfoDTO(user=UserDTO(username=user.username),
                              user_info=user_info)


@router.put('/me')
async def update_profile(updated_user: UserInfoDTO, user: User = Depends(get_user_by_jwt_token)):
    user_info = update_user_info(user.id, updated_user)
    return UserVerboseInfoDTO(user=UserDTO(username=user.username),
                              user_info=user_info)
