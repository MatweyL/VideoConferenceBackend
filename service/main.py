from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from conference.router import router as conference_router
from user.router import router as auth_router
from user_info.router import router as user_router

fastapi_app = FastAPI()
origins = ["*"]
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
fastapi_app.include_router(auth_router, prefix='/users')
fastapi_app.include_router(user_router, prefix='/users')
fastapi_app.include_router(conference_router, prefix='/conferences')

# socketio_app = socketio.ASGIApp(sio, fastapi_app)
app = fastapi_app
