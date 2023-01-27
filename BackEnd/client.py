import pickle
import socket
import time
from request import Request


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 2701
        self.address = (self.host, self.port)
        self.connect()
        self.username = ""

    def connect(self):
        self.client.connect(self.address)

    def disconnect(self):
        self.client.close()

    def set_username(self, username):
        self.username = username

    def send(self, msg, data, return_response):
        request = Request(msg, data)
        start_time = time.time()
        while time.time() - start_time < 15:
            try:
                if return_response:
                    self.client.send(pickle.dumps(request))
                    response = self.client.recv(4096 * 128)
                    try:
                        response_data = pickle.loads(response)
                        return response_data
                    except Exception as e:
                        print(e)
                else:
                    self.client.send(pickle.dumps(request))
                    self.client.recv(4096 * 128)
                    return
            except socket.error as e:
                print(e)
