# chat_client/client.py
import socketio

sio = socketio.Client()
username = ""
room = ""
SERVER_URL = "https://chat-server-6xmo.onrender.com"  # Fixed server URL

@sio.event
def connect():
    print("[CONNECTED]")

@sio.event
def disconnect():
    print("[DISCONNECTED]")

@sio.on("message")
def on_message(data):
    # Show only messages from others
    if isinstance(data, dict) and "message" in data and "username" in data:
        if data["username"] != username:
            print(f"\n{data['username']}: {data['message']}")
    else:
        print(f"\n{data}")

def join_chat(user, room_id):
    global username, room
    username = user
    room = room_id
    sio.connect(SERVER_URL)
    sio.emit("join", {"username": username, "room": room})
    print(f"[JOINED ROOM {room}] Type your messages below.")
    print("Type ':send' on a new line to send multi-line messages. Type 'exit' or 'quit' to leave.")

    try:
        while True:
            lines = []
            while True:
                line = input()
                if line.strip() in ("exit", "quit") and not lines:
                    return
                if line.strip() == ":send":
                    break
                lines.append(line)
            msg = "\n".join(lines)
            if msg.strip() != "":
                sio.emit("message", {"username": username, "room": room, "message": msg})
    finally:
        sio.emit("leave", {"username": username, "room": room})
        sio.disconnect()
