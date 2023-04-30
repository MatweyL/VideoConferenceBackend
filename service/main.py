from fastapi import FastAPI, HTTPException

from crud import crud_manager
from dto import UserDTO, AccessToken
from exceptions import UsernameAlreadyExistsError, UserNotExistingError
from models import User
from services import create_access_token, get_password_hash

app = FastAPI()


@app.get('/ping')
async def ping():
    return {'message': 'pong'}


@app.post('/users/register', status_code=201, response_model=User)
async def register_user(user: UserDTO):
    try:
        user_to_create = User(username=user.username, password_hashed=get_password_hash(user.password))
        user_db: User = crud_manager.crud(User).create(user_to_create)
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=409, detail=f"Username {user.username} already registered")
    else:
        return user_db


@app.post('/users/auth', status_code=200, response_model=AccessToken)
async def authenticate_user(user: UserDTO):
    try:
        user_db: User = crud_manager.crud(User).read(user.username)
    except UserNotExistingError:
        raise HTTPException(status_code=403, detail=f"Wrong username or password")
    else:
        return create_access_token(user_db.username)


async def get_profile():
    pass
