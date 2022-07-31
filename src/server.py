import socket
from _thread import *

server = "192.168.0.3"
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
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            answer = data.decode("utf-8")
            reply = "Working"
            if not data or answer == "Goodbye":
                print("Disconnected")
                break
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
