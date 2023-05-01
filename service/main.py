from fastapi import FastAPI, Depends

from auth.router import router as auth_router
from auth.service import get_user_by_jwt_token
from models import User
from schemas import UserDTO

app = FastAPI()

app.include_router(auth_router)


@app.get('/ping')
async def ping():
    return {'message': 'pong'}


@app.get('/users/me')
async def get_profile(user: User = Depends(get_user_by_jwt_token)):
    return UserDTO(username=user.username)


@app.put('/users/me')
async def update_profile(updated_user: UserDTO = None, user: User = Depends(get_user_by_jwt_token)):
    return UserDTO(username=user.username)
