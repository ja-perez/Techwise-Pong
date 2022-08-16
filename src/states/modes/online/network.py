import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Testing
        local_server = socket.gethostbyname(socket.gethostname())
        self.server = str(local_server)
        # Testing
        # Raspberry Pi Server - unofficial server
        # self.server = "192.168.0.150"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
            return pickle.loads(self.client.recv(2048))
        except:
            print("Couldn't connect")
            self.connected = False

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)


    def disconnect(self):
        self.client.send(str.encode("goodbye"))
