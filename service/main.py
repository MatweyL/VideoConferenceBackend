from fastapi import FastAPI, HTTPException

from fastapi import FastAPI, HTTPException

from service.crud import crud_manager
from service.exceptions import UsernameAlreadyExistsError, UserNotExistingError
from service.models import User, AccessToken, UserDTO
from service.services import create_access_token

app = FastAPI()


@app.get('/ping')
async def ping():
    return {'message': 'pong'}


@app.post('/users/register', status_code=201, response_model=User)
async def register_user(user: UserDTO):
    try:
        user_db = crud_manager.crud_manager(User).create(user)
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=409, detail=f"Username {user.username} already registered")
    else:
        return user_db


@app.post('/users/auth', status_code=200, response_model=AccessToken)
async def authenticate_user(user: UserDTO):
    try:
        user_db = crud_manager.crud_manager(User).read(user.username)
    except UserNotExistingError:
        raise HTTPException(status_code=403, detail=f"Wrong username or password")
    else:
        return create_access_token(user)
