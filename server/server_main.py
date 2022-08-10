import socket

from pong_server import Pong_Server

# Raspberry Pi Server IP
server = "192.168.0.150"
port = 5555
queue = 2

def main():
    s = Pong_Server(server, port, queue)
    s.server_conn()


if __name__ == "__main__":
    main()
