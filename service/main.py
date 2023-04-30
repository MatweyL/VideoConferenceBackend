import logging
import random
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends

from crud import crud_manager
from dto import UserCredentialsDTO, AccessToken, UserDTO
from exceptions import UsernameAlreadyExistsError, UserNotExistingError
from models import User
from services import create_access_token, get_password_hash, get_user_by_credentials, get_user_by_jwt_token

app = FastAPI()


@app.get('/ping')
async def ping():
    return {'message': 'pong'}


@app.post('/users/register', status_code=201, response_model=UserDTO)
async def register_user(user: UserCredentialsDTO):
    try:
        user_to_create = User(username=user.username, password_hashed=get_password_hash(user.password))
        user_db: User = crud_manager.crud(User).create(user_to_create)
        user_created = UserDTO(username=user_db.username)
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=409, detail=f"Username {user.username} already registered")
    else:
        return user_created


@app.post('/users/auth', status_code=200, response_model=AccessToken)
async def authenticate_user(user: UserCredentialsDTO):
    try:
        user_db: User = get_user_by_credentials(user)
    except UserNotExistingError:
        raise HTTPException(status_code=403, detail=f"Wrong username or password")
    else:
        return create_access_token(user_db.username)


@app.get('/users/me')
async def get_profile(user: UserDTO = Depends(get_user_by_jwt_token)):
    return user
