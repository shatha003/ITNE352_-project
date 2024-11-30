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
    
    def run(self):
        #run the client loop and handle user input. 
        while True:
            try:
                self.display_request_types()
                request_type_num = int(input("Enter request type (1-3): "))

                if 1 <= request_type_num <= len(self.request_types):
                    request_type = self.request_types[request_type_num - 1]

                    if request_type == "Search Headlines":
                        self.search_headlines()
                    elif request_type == "List Sources":
                        self.list_sources()
                    elif request_type == "Quit":
                        print("See you, Goodbye!")
                        break
                else:
                    print("Invalid request type.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        

