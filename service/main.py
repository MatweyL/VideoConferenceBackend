import datetime
from hashlib import md5

from fastapi import FastAPI, HTTPException

from service.crud import CRUDFacade
from service.exceptions import UsernameAlreadyExistsError, UserNotExistingError
from service.models import User, Token

app = FastAPI()
crud = CRUDFacade()


def get_token(user: User) -> Token:
    return Token(token=md5(f'{user.username}{user.password}{datetime.datetime.now()}'.encode()).hexdigest(), type='bearer')

@app.get('/ping')
async def ping():
    return {'message': 'pong'}


@app.post('/users/register', status_code=201, response_model=User)
async def register_user(user: User):
    try:
        crud_user = crud.crud(User).create(user)
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=409, detail=f"Username {user.username} already registered")
    else:
        return crud_user


@app.post('/users/auth', status_code=200, response_model=Token)
async def authenticate_user(user: User):
    try:
        crud_user = crud.crud(User).read(user.username)
    except UserNotExistingError:
        raise HTTPException(status_code=403, detail=f"Wrong username or password")
    else:
        return get_token(user)
