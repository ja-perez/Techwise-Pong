import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Testing
        local_server = socket.gethostbyname(socket.gethostname())
        self.server = str(local_server)
        # Testing
        # self.server = "192.168.56.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        self.friend_code = ""

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
            return self.client.recv(2048).decode()
        except:
            print("Couldn't connect")
            self.connected = False

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            self.connected = False

    def disconnect(self):
        self.client.send(str.encode("Goodbye"))
