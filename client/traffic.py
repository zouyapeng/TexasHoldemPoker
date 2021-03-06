'''
    Class for communication with remote server (core)
'''
import socketserver
import json
import requests

class Sender():
    
    def __init__(self, client):
        self.client = client
        self.remote_server = "http://localhost:8080"
    
    def register_player(self, address, name):
        requests.post(self.remote_server + "/registerPlayer", 
                            data={'name': name, 'address': address})

    def get_players(self):
        r = requests.get(self.remote_server + "/inGame")
        data = json.loads(r.text)
        self.client.init_table(data)

    def take_seat(self, address, number):
        r = requests.post(self.remote_server + "/takeSeat", 
                            data={'seat': number, 'address': address})
        data = json.loads(r.text)
        if(data):
            self.client.draw_empty_seats(data)

    def check(self):
        print("check")

    def call(self, call_value, seat):
        r = requests.post(self.remote_server + "/call", 
                            data={'call': int(call_value), 'seat': int(seat)})
        data = json.loads(r.text)
        self.client.init_table(data)

    def raise_to(self, raise_value):
        print("raise to "+ str(raise_value))

    def bet_to(self, bet_value):
        print("bet to "+ str(bet_value))
    
    def fold(self):
        print("fold")

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self, client):
        self.client = client

    def __call__(self, request, client_address, server):
        h = MyTCPHandler(self.client)
        socketserver.BaseRequestHandler.__init__(h, request, client_address, server)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(2096).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        
        try:
            data = self.data.decode('UTF-8').split('\r\n\r\n')[1] #split request with new line (header is at position 0, data is at position 1)
        except IndexError:
            data = self.request.recv(2096).strip()
            print(self.data)

        data = json.loads(data)
        self.client.data = data

        for x in data:
            self.client.refresh_table(x)

        response = b'HTTP/1.1 200 OK\n\n'
        self.request.sendall(response)