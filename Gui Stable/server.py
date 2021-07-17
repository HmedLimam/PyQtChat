import socket
from threading import Thread
import time
import re

#TODO : ADD DATABASE SQLALCHEMY FOR REGISTRATION AND LOGIN
#TODO : FIX USER LIMITATION
#TODO CLIENT : UNIQUE NAME REQUIRED
#TODO CLIENT : FIX HTML TAGS IN CHAT
#TODO WWW : Add index / hide Output

dic = {
                "[007]": "┌( ͝° ͜ʖ͡°)=ε/̵͇̿̿/’̿’̿ ̿",
                "[check]": "✔",
                "[angry]": "•`_´•",
                "[koala]": "ʕ·͡ᴥ·ʔ",
                "[idk]": "¯\_(ツ)_/¯",
                "[hug]": "(づ￣ ³￣)づ",
                "[letsgo]": "(งツ)ว",
                "[<3]": "♥",
                "[taco]": "🌮",
                "[cry]": "(╥﹏╥)",
            }

HOST = input("HOST : ")
PORT = input('PORT : ')

if not HOST:
    HOST = '192.168.1.123'

if not PORT:
    PORT = 420

PORT = int(PORT)

clients = {} # holds client's name
addresses = {} # holds client's address

server_addr = (HOST, PORT)
print(server_addr)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_addr)
server.listen(20)

print("Server started.\nWaiting for connections..")

def send_server_message():
    while True:
        try:
            msg = input('')
            if msg:
                broadcast(f"<h4 style='color:#800080'>server: {msg}</h4>******server******".encode())
            time.sleep(0.5)
        except ConnectionAbortedError:
            continue

def accept_incoming_connections():
    while True:
        try:
            client, addr = server.accept()
            addresses[client] = addr
            print(f"{addr} has connected to the server.")
            Thread(target=handle_client, args=(client,), daemon=True).start()
        except ConnectionAbortedError:
            continue

def handle_client(client):
    name = client.recv(1024)
    clients[client] = name.decode() # defining this here means all the broadcasts after, are sent to the client.
    ad = f"{addresses[client][0]}:{addresses[client][1]}"
    client.send(ad.encode())
    # time.sleep(0.5)
    # number = str(len(clients))
    # client.send(number.encode())
    time.sleep(0.1)
    client.send(b"Welcome to chat!")
    time.sleep(0.1)
    broadcast(f"<span style=\" color: #008000;\">{name.decode()} has connected to the server.</span>".encode()) #
    # if clients[client] = name.decode() was here, then the client connecting will not receive the client has connected to the server message.

    while True:
        try:
            try:
                msg = client.recv(1024)
                if msg.startswith(b"/q"):
                    broadcast(f"<span style=\" color: #0000FF;\">{name.decode()} has left the chat.</span>".encode())
                    print(f"{addresses[client]} has disconnected from the server.")
                    client.close()
                    del clients[client]
                    break

                elif msg.startswith(b"/ra"):
                    broadcast(
                        f"<span style=\" color: #ff0000;\">{name.decode()} is ringing everyone!******ring******</span>".encode())

                elif msg.startswith(b"/r"):
                    r_pattern = re.compile(r"(/r) ([\d\w\s]*)")
                    msg = msg.decode()
                    try:
                        r_match = r_pattern.findall(msg)[0]

                        send_to = r_match[1].strip()

                        if send_to:
                            if send_to == name.decode():
                                client.send(
                                    f"<span style=\" color: #8B0000;\">You can't ring yourself ʕ·͡ᴥ·ʔ.</span>".encode())
                            else:
                                if send_to in clients.values():
                                    send_to_person(
                                        f"<span style=\" color: #800080;\">{name.decode()} is ringing you!******ring******</span>".encode(),
                                        send_to)
                                    time.sleep(0.1)
                                    client.send(
                                        f"<i><span style=\" color: #c0c6c8;\">You ringed {send_to}.</span></i>".encode())
                                else:
                                    client.send(
                                        f"<span style=\" color: #8B0000;\">{send_to} is offline.</span>".encode())

                        else:
                            pass
                    except IndexError:
                        pass

                elif msg.startswith(b"/p"):
                    p_pattern = re.compile(r"(/p) \(([\d\w\s]*)\) (.*)")
                    msg = msg.decode()
                    try:
                        p_match = p_pattern.findall(msg)[0]

                        send_to = p_match[1].strip()
                        private_msg = p_match[2]

                        if send_to and private_msg:
                            if send_to == name.decode():
                                client.send(
                                    f"<span style=\" color: #8B0000;\">You can't send a private message to yourself ʕ·͡ᴥ·ʔ.</span>".encode())
                            else:
                                if send_to in clients.values():
                                    final = ""
                                    for word in private_msg.split():
                                        final += dic.get(word, word) + " "
                                    client.send(
                                        f"<span style=\" color: #FF00FF;\">To {send_to}: {final}</span>".encode())
                                    time.sleep(0.1)
                                    send_to_person(
                                        f"<span style=\" color: #FF00FF;\">From {name.decode()}: {final}******pm******</span>".encode(),
                                        send_to)
                                else:
                                    client.send(
                                        f"<span style=\" color: #8B0000;\">{send_to} is offline.</span>".encode())

                        else:
                            pass
                    except IndexError:
                        continue

                else:
                    broadcast(f"<span style=\" color: #ff0000;\">{name.decode()}</span>: {msg.decode()}".encode())
            except ConnectionResetError:
                continue

        except ConnectionAbortedError:
            continue

def send_updates():
    while True:
        try:
            msg = (f"#/#{len(clients)}##  */*{clients.values()}**".encode())
            time.sleep(0.5)
            broadcast(msg)
        except ConnectionAbortedError:
            continue


def broadcast(msg):
    for sock in clients:
        try:
            final = ""
            for word in msg.decode().split():
                final += dic.get(word,word) + " "
            sock.send(final.encode())
        except ConnectionResetError:
            pass
        except ConnectionAbortedError:
            continue

def send_to_person(msg, name):
    for sock in clients:
        try:
            if clients[sock] == name:
                final = ""
                for word in msg.decode().split():
                    final += dic.get(word, word) + " "
                sock.send(final.encode())
            else:
                pass
        except ConnectionResetError:
            pass
        except ConnectionAbortedError:
            continue


T = Thread(target=accept_incoming_connections, daemon=True)
T.start()
Thread(target=send_server_message, daemon=True).start()
Thread(target=send_updates, daemon=True).start()
T.join()