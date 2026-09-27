# Visit the Snail Mail garden and send notes by snail.
# Type a message and press Enter. Type "bye" to leave.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

mailbox = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mailbox.connect((HOST, PORT))


def listen_for_snails():
    while True:
        data = mailbox.recv(1024)
        if not data:
            print("🥀 The garden gate has closed. Goodbye!")
            break
        print(data.decode(), end="")


ears = threading.Thread(target=listen_for_snails, daemon=True)
ears.start()

while True:
    note = input()
    if note == "bye":
        break
    mailbox.sendall((note + "\n").encode())

print("👋 You tiptoe out of the garden. The snails wave goodbye (slowly).")
