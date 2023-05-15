from fastapi import FastAPI

from user.router import router as auth_router
from user_info.router import router as user_router
from conference.router import router as conference_router

app = FastAPI()

app.include_router(auth_router, prefix='/users')
app.include_router(user_router, prefix='/users')
app.include_router(conference_router, prefix='/conferences')


@app.get('/ping')
async def ping():
    return {'message': 'pong'}
