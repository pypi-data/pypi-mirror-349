# cli.py
import argparse
import subprocess
from chat_client import client

def main():
    parser = argparse.ArgumentParser(description="Terminal Chat Room")
    parser.add_argument("command", nargs="?", help="Command to run: join or --setup")
    parser.add_argument("room", nargs="?", help="Room ID to join")
    parser.add_argument("username", nargs="?", help="Your username")

    args = parser.parse_args()

    if args.command == "--setup":
        print("[INFO] Installing dependencies...")
        subprocess.call(["pip", "install", "-r", "requirements.txt"])
        print("[DONE] Setup complete.")
    elif args.command == "join" and args.room and args.username:
        client.join_chat(args.username, args.room)
    else:
        print("Usage:")
        print("  room --setup")
        print("  room join <room_id> <username>")
