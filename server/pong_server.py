import socket
import _thread
import random
import pickle
from match import Match_Manager


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
        # TODO: Change to create matches by request instead of pre-emptively #
        if self.num_of_clients % 2 > self.m.number_of_matches():
            self.m.create_match()
        _thread.start_new_thread(self.threaded_client, (conn, client_id))

    def threaded_client(self, conn, client_id):

        client_conn_msg = "ClientID: " + str(client_id)
        conn.send(pickle.dumps(client_conn_msg))
        curr_match = None
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                if "stop" not in data:
                    print(str(client_id) + " received:", data)
                if not data or data.lower() == "goodbye":
                    break
                if type(curr_match) == int:
                    reply = self.m.update_match(curr_match, client_id, data)
                    if reply == "goodbye":
                        curr_match = None
                else:
                    reply = self.process_client_data(data, client_id)
                    if type(reply) == dict:
                        curr_match = int(reply["match_id"])
                    else:
                        reply = str(reply)
                    if reply:
                        print(str(client_id) + " reply:", reply)
                self.m.update_matches()
                conn.sendall(pickle.dumps(reply))
            except:
                break
        if curr_match:
            self.m.update_match(curr_match, client_id, "goodbye")
        self.num_of_clients -= 1
        self.client_ids.remove(client_id)
        self.m.update_matches()
        print("Lost connection")
        conn.close()

    def process_client_data(self, data: str, client_id: int):
        if data == "create_private":
            private_state = self.m.create_private_match(client_id)
            return private_state
        elif "join_private" in data:
            private_state = self.m.get_private_match(data.split()[1], client_id)
            return private_state
        elif data == "join_public":
            public_state = self.m.get_open_match(client_id)
            return public_state
        else:
            return "No action available"

    def get_client_id(self) -> int:
        while True:
            random.seed()
            client_id = random.randint(1000, 9999)
            if client_id not in self.client_ids:
                self.client_ids.add(client_id)
                break
        return client_id
