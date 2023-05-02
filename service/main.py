from fastapi import FastAPI

from auth.router import router as auth_router
from user.router import router as user_router
import database

app = FastAPI()

app.include_router(auth_router, prefix='/users')
app.include_router(user_router, prefix='/users')


@app.get('/ping')
async def ping():
    return {'message': 'pong'}
