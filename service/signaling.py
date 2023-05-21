import socketio

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

users_in_room = {}
rooms_sid = {}
names_sid = {}
names_sid_mapping = {}


def get_users_sids_in_room(room_id):
    return users_in_room[room_id] if users_in_room.get(room_id) else []


@sio.on("connect")
def on_connect(sid, *args, **kwargs):
    print("New socket connected ", sid)
    print("\nusers: ", users_in_room, "\n")


@sio.on("join-room")
async def on_join_room(sid, data):
    room_id = data["room_id"]
    display_name = data["name"]
    print(f"USER {display_name} ENTERING TO {room_id} ")
    # register sid to the room
    if display_name in names_sid_mapping:
        print(f"Detected page reloading in {display_name}")
        await leave_from_call(names_sid_mapping[display_name], room_id)
    sio.enter_room(sid, room_id)
    rooms_sid[sid] = room_id
    names_sid[sid] = display_name
    names_sid_mapping[display_name] = sid

    # broadcast to others in the room
    print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
    await sio.emit("user-connect", {"sid": sid, "name": display_name},
             skip_sid=True, room=room_id)

    # add to user list maintained on server
    if room_id not in users_in_room:
        users_in_room[room_id] = [sid]
        await sio.emit("user-list", {"my_id": sid})  # send own id only
    else:
        usrlist = {u_id: names_sid[u_id]
                   for u_id in users_in_room[room_id] if u_id in names_sid}
        # send list of existing users to the new member
        await sio.emit("user-list", {"list": usrlist, "my_id": sid})
        # add new member to user list maintained on server
        users_in_room[room_id].append(sid)

    print("\nusers: ", users_in_room, "\n")


@sio.on("disconnect")
async def on_disconnect(sid):
    try:
        room_id = rooms_sid[sid]
        display_name = names_sid[sid]
    except KeyError:
        return

    print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    await leave_from_call(sid, room_id)

    print("\nusers: ", users_in_room, "\n")


async def leave_from_call(sid, room_id):
    await sio.emit("user-disconnect", {"sid": sid},
         skip_sid=True, room=room_id)
    try:
        users_in_room[room_id].remove(sid)
    except BaseException as e:
        print(f"WARNING (users_in_room[room_id].remove(sid)): {e}")
    try:
        if len(users_in_room[room_id]) == 0:
            users_in_room.pop(room_id)
    except BaseException as e:
        print(f"WARNING (if len(users_in_room[room_id]) == 0:): {e}")

    sio.leave_room(sid, room_id)
    try:
        rooms_sid.pop(sid)
    except BaseException as e:
        print(e)
    try:
        names_sid.pop(sid)
    except BaseException as e:
        print(e)


@sio.on("data")
async def on_data(sid, data):
    sender_sid = data['sender_id']
    target_sid = data['target_id']
    if sender_sid != sid:
        print("[Not supposed to happen!] request.sid and sender_id don't match!!!")

    if data["type"] != "new-ice-candidate":
        print('{} message from {} to {}'.format(
            data["type"], sender_sid, target_sid))
    await sio.emit('data', data, room=target_sid)
