from fastapi import APIRouter, HTTPException

from user.errors import UsernameAlreadyExistsError, UserNotExistingError, AuthenticationError
from user.schemas import UserCredentialsDTO, AccessToken
from user.service import create_access_token, get_user_by_credentials, create_user
from models import User
from schemas import UserDTO

router = APIRouter()


@router.post('/register', status_code=201, response_model=UserDTO)
async def register_user(user: UserCredentialsDTO):
    try:
        user_created: UserDTO = create_user(user)
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=409, detail=f"Username {user.username} already registered")
    else:
        return user_created


@router.post('/auth', status_code=200, response_model=AccessToken)
async def authenticate_user(user: UserCredentialsDTO):
    try:
        user_db: User = get_user_by_credentials(user)
    except (UserNotExistingError, AuthenticationError):
        raise HTTPException(status_code=403, detail=f"Wrong username or password")
    else:
        return create_access_token(user_db.username)
