import socket

from pong_server import Pong_Server

# Temp
local_server = socket.gethostbyname(socket.gethostname())
server = str(local_server)
port = 5555
queue = 2
# Temp

def main():
    s = Pong_Server(server, port, queue)
    s.server_conn()


if __name__ == "__main__":
    main()
