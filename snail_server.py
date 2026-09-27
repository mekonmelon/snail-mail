# SNAIL MAIL: the world's slowest chat room.
# Every message is carried by a tiny snail (a thread!) who takes its sweet time.

import socket
import threading
import random
import time

HOST = "127.0.0.1"
PORT = 5050

SNAILS = ["Gary", "Turbo", "Sir Slime-a-Lot", "Lightning", "Professor Goo", "Shellby"]
DISTRACTIONS = [
    "stopped to admire a very nice leaf",
    "took a quick nap in a puddle",
    "got into an argument with a mushroom",
    "paused to write a poem about dew",
    "waved hello to a passing worm",
    "forgot where it was going, then remembered",
]

garden = []
garden_lock = threading.Lock()


def tell_everyone(message):
    print(message, end="")
    with garden_lock:
        for friend in garden:
            try:
                friend.sendall(message.encode())
            except OSError:
                pass


def snail_trip(sender, text):
    snail = random.choice(SNAILS)
    trip_time = random.randint(4, 10)
    tell_everyone(f"🐌 {snail} picked up a note from {sender} and started crawling...\n")
    time.sleep(trip_time / 2)
    tell_everyone(f"🍃 Halfway there, {snail} {random.choice(DISTRACTIONS)}.\n")
    time.sleep(trip_time / 2)
    if random.randint(1, 10) == 1:
        tell_everyone(f"🥬 Oh no! {snail} got hungry and ate {sender}'s note. It tasted like '{text}'.\n")
    else:
        tell_everyone(f"📬 {snail} arrived after {trip_time} whole seconds! {sender} says: {text}\n")


def welcome_visitor(conn):
    conn.sendall("🌿 Welcome to Snail Mail, the slowest chat in the world! What's your name?\n".encode())
    name = conn.recv(1024).decode().strip()
    if name == "":
        name = "A Mysterious Pebble"
    with garden_lock:
        garden.append(conn)
    tell_everyone(f"🍄 {name} has wandered into the garden.\n")

    while True:
        try:
            data = conn.recv(1024)
        except OSError:
            break
        if not data:
            break
        text = data.decode().strip()
        snail = threading.Thread(target=snail_trip, args=(name, text), daemon=True)
        snail.start()

    with garden_lock:
        garden.remove(conn)
    conn.close()
    tell_everyone(f"🍂 {name} has left the garden. The snails will miss them.\n")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"🐌 The Snail Mail post office is open at {HOST}:{PORT}")

while True:
    conn, address = server.accept()
    print(f"🌱 Someone new arrived from {address}")
    visitor = threading.Thread(target=welcome_visitor, args=(conn,), daemon=True)
    visitor.start()
