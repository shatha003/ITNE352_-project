import socket
import json
import requests
from rich.console import Console

class NewsClient:
    def __init__(self, host, port):
        #Initialize the client, connect to the server and set up the necessary variables.
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_name = input("Enter your name: ")
        self.client_socket.sendall(self.client_name.encode())
        self.request_types = ["Search Headlines", "List Sources", "Quit"]

        
