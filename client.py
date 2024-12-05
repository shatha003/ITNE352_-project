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
        self.client_socket.settimeout(10)  # Timeout in seconds
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
                        self.client_socket.sendall("quit".encode())
                        break
                else:
                    print("Invalid request type.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    
    def display_request_types(self):
        #Display the list of main request types (options) for the user.
        print("Request Types:")
        for i, request_type in enumerate(self.request_types, start=1):
            print(f"{i}. {request_type}")
    
    def search_headlines(self):
        # handle searching for headlines based on various criteria.
        while True:
            self.display_headline_submenu_types()
            submenu_type_num = int(input("Enter submenu type (1-6): "))

            if 1 <= submenu_type_num <= len(self.headline_submenu_types):
                submenu_type = self.headline_submenu_types[submenu_type_num - 1]
                self.process_headline_submenu_type(submenu_type)
            else:
                print("Invalid headline submenu type.")

    def display_headline_submenu_types(self):
        #Display the list of submenus available for headline search.
        print("Headline Submenu Types:")
        self.headline_submenu_types = ["country", "category", "language", "sources", "keyword", "page_size", "Back to main menu"]
        for i, submenu_type in enumerate(self.headline_submenu_types, start=1):
            print(f"{i}. {submenu_type}")
    
    def process_headline_submenu_type(self, submenu_type):
        #Process the submenu input and fetch headlines accordingly.
        if submenu_type == "Back to main menu":
            return
        
        value = input(f"Enter {submenu_type} please: ")
        self.fetch_headlines(submenu_type, value)

    
    def fetch_headlines(self, submenu_type, value):
        request = json.dumps({"option": "headlines", "params": {submenu_type: value}})
        self.client_socket.sendall(request.encode())

        response = json.loads(self.client_socket.recv(1024).decode())

        if isinstance(response, list):  # Successful response
             for item in response:
                 print(f"- {item['title']} (Source: {item['source_name']})")  # For headlines
        else:  # Error response
            print("Error:", response.get('message', 'Unknown error'))

    

    def list_sources(self):
        #Method to handle listing sources based on user criteria.
        while True:
            self.display_source_submenu_types()
            submenu_type_num = int(input("Enter submenu type (1-4): "))

            if 1 <= submenu_type_num <= len(self.source_submenu_types):
                submenu_type = self.source_submenu_types[submenu_type_num - 1]
                self.fetch_sources(submenu_type)
            else:
                print("Invalid source submenu type.")
    

    def display_source_submenu_types(self):
        #Display the list of submenus available for listing sources.
        print("Source Submenu Types:")
        self.source_submenu_types = ["category", "language", "country", "Back to main menu"]
        for i, submenu_type in enumerate(self.source_submenu_types, start=1):
            print(f"{i}. {submenu_type}")


    def fetch_sources(self, submenu_type):
        #Fetch the sources based on the selected submenu type.
        if submenu_type == "category":
            value = input("Enter (category) please: ")
        elif submenu_type == "language":
            value = input("Enter (language) please: ")
        elif submenu_type == "country":
            value = input("Enter (country) please: ")
        else:
            return
        
        request = json.dumps({"option": "sources", "params": {submenu_type: value}})
        
        # Send the request to the server
        self.client_socket.sendall(request.encode())

        # Receive the response from the server
        response = json.loads(self.client_socket.recv(1024).decode())

        # Display the fetched sources
        if response.get('status') == 'ok':
            Console().print(f"[bold green]Fetched {len(response['sources'])} sources![/bold green]")
            for source in response['sources']:
                print(f"- {source['name']} (Category: {source['category']}, Language: {source['language']}, Country: {source['country']})")
        else:
            print("No sources found or error in request.")


if __name__ == "__main__":
    HOST = '127.0.0.1'  
    PORT = 12346
    news_client = NewsClient(HOST, PORT)  
    news_client.run()  



        

