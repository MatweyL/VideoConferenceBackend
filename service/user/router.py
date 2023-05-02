from fastapi import APIRouter, Depends

from auth.service import get_user_by_jwt_token
from models import User
from schemas import UserDTO

router = APIRouter()

@router.get('/me')
async def get_profile(user: User = Depends(get_user_by_jwt_token)):
    return UserDTO(username=user.username)


@router.put('/me')
async def update_profile(updated_user: UserDTO = None, user: User = Depends(get_user_by_jwt_token)):
    return UserDTO(username=user.username)
