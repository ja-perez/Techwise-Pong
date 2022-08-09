import socket
import _thread
import random
from match import Match_Manager

"""
TODO:
Implement Basic Entity Creation per match
"""

class Pong_Server():
    def __init__(self, server_ip, port, queue):
        self.server_ip, self.port, self.queue = server_ip, port, queue
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_socket()
        self.matches = {}
        self.num_of_clients, self.client_ids = 0, set()
        self.m = Match_Manager()

    def bind_socket(self):
        try:
            self.s.bind((self.server_ip, self.port))
        except socket.error as e:
            return str(e)

    def server_conn(self):
        self.s.listen(self.queue)
        print("Waiting for a connection, Server Started")
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            self.m.print_matches()
            self.num_of_clients += 1
            self.create_client_thread(conn)

    def create_client_thread(self, conn):
        client_id = self.get_client_id()
        if self.num_of_clients % 2 > self.m.number_of_matches():
            # TODO: Create matches by request instead of making them "statically" #
            self.m.create_match()
        _thread.start_new_thread(self.threaded_client, (conn, client_id))

    def threaded_client(self, conn, client_id):
        conn.send(str.encode("ClientID:" + " " + str(client_id)))
        curr_match = None
        while True:
            try:
                data = conn.recv(2048)
                data = data.decode("utf-8")
                print(str(client_id) + " received:", data)
                if not data or data.lower() == "goodbye":
                    if curr_match:
                        self.m.update_match(curr_match, client_id, data)
                    break
                reply = ""
                if type(curr_match) == int:
                    reply = self.m.update_match(curr_match, client_id, data)
                else:
                    reply = self.process_client_data(data, client_id)
                    curr_match = reply
                    reply = str(reply)
                    print(str(client_id) + " reply:", reply)
                self.m.update_matches()
                conn.sendall(str.encode(reply))
            except:
                break

        self.num_of_clients -= 1
        self.client_ids.remove(client_id)
        self.m.update_matches()
        print("Lost connection")
        conn.close()

    def process_client_data(self, data: str, client_id: int):
        if data == "create_private":
            self.m.create_private_match(client_id)
            return client_id
        elif "join_private" in data:
            private_id = self.m.get_private_match(data.split()[1], client_id)
            return private_id
        elif data == "join_public":
            public_id = self.m.get_open_match(client_id)
            return public_id
        else:
            return "No action available"

    def get_client_id(self):
        while True:
            random.seed()
            client_id = random.randint(1000, 9999)
            if client_id not in self.client_ids:
                self.client_ids.add(client_id)
                break
        return client_id
