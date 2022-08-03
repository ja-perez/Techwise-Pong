import socket
import random
from _thread import *

# Testing
local_server = socket.gethostbyname(socket.gethostname())
server = str(local_server)
# Testing
#server = "192.168.56.1"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

"""
moves = ["false false", "false false"]
def threaded_client(conn, curr_player):
    conn.send(str.encode(moves[curr_player]))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            moves[curr_player] = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                if curr_player == 0:
                    reply = moves[1]
                else:
                    reply = moves[0]

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()
"""

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    random.seed()
    friend_code = random.randint(1000, 9999)
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            answer = data.decode("utf-8")
            reply = answer
            if not data or answer == "Goodbye":
                print("Disconnected")
                break
            elif answer == "friendcode":
                reply = str(friend_code)
            elif answer == "test":
                reply = ""
            else:
                print("Received:", answer)
                print("Sending :", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

#curr_player = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
#    start_new_thread(threaded_client, (conn, curr_player))
#    curr_player += 1
