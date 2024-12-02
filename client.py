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
        self.headline_submenu_types = ["country", "category", "language", "sources", "keyword", "page_size"]
        for i, submenu_type in enumerate(self.headline_submenu_types, start=1):
            print(f"{i}. {submenu_type}")
    
    def process_headline_submenu_type(self, submenu_type):
        #Process the submenu input and fetch headlines accordingly.
        if submenu_type == "country":
            country = input("Enter (country) please: ")
            self.fetch_headlines(submenu_type, country)
        elif submenu_type == "category":
            category = input("Enter (category) please: ")
            self.fetch_headlines(submenu_type, category)
        elif submenu_type == "language":
            language = input("Enter (language) please: ")
            self.fetch_headlines(submenu_type, language)
        elif submenu_type == "sources":
            sources = input("Enter (sources) please: ")
            self.fetch_headlines(submenu_type, sources)
        elif submenu_type == "keyword":
            keyword = input("Enter (keyword) please: ")
            self.fetch_headlines(submenu_type, keyword)
        elif submenu_type == "page_size":
            page_size = input("Enter (page size) please: ")
            self.fetch_headlines(submenu_type, page_size)
    
    def fetch_headlines(self, submenu_type, value):
        #Fetch the headlines based on submenu type and value, then print the results. 
        request = f"Search Headlines;{submenu_type};{value}"

        # Send the request to the server
        self.client_socket.sendall(request.encode())

        # Receive the response from the server
        response = json.loads(self.client_socket.recv(1024).decode())

        # Display the fetched headlines
        if response.get('status') == 'ok':
            Console().print(f"[bold green]Fetched {len(response['articles'])} headlines![/bold green]")
            for article in response['articles']:
                print(f"- {article['title']} (Source: {article['source']['name']}, Author: {article['author']})")
        else:
            print("No articles found or error in request.")
    

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
            category = input("Enter (category) please: ")
            request = f"List Sources;{submenu_type};{category}"
        elif submenu_type == "language":
            language = input("Enter (language) please: ")
            request = f"List Sources;{submenu_type};{language}"
        elif submenu_type == "country":
            country = input("Enter (country) please: ")
            request = f"List Sources;{submenu_type};{country}"
        else:
            return

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
    HOST = 'localhost'  
    PORT = 4000         
    news_client = NewsClient(HOST, PORT)  
    news_client.run()  



        

