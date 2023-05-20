import socketio

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')


@sio.event
def connect(sid, environ, *args, **kwargs):
    print("connect ", sid)
    print(*args, **kwargs)


@sio.event
def init(sid,  *args, **kwargs):
    print("init ", *args, **kwargs)


