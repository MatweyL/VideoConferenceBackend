from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from user.router import router as auth_router
from user_info.router import router as user_router
from conference.router import router as conference_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix='/users')
app.include_router(user_router, prefix='/users')
app.include_router(conference_router, prefix='/conferences')


@app.get('/ping')
async def ping():
    return {'message': 'pong'}
