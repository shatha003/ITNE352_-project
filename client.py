import socket
import json

class NewsClient:
    def _init_(self, host, port):
        # Initialize the client, connect to the server, and set up necessary variables.
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_name = input("Enter your name: ")
        self.client_socket.sendall(self.client_name.encode())
        self.points = 0  # Initialize points
        self.main_menu()

    def main_menu(self):
        # Run the client loop and handle user input.
        while True:
            print("\nMain Menu:")
            print("1. Search Headlines")
            print("2. List Sources")
            print("3. View Points")  # New option to view points
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.search_headlines()
            elif choice == "2":
                self.list_sources()
            elif choice == "3":
                self.view_points()  # Call view_points function
            elif choice == "4":
                self.client_socket.sendall("quit".encode())
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    def search_headlines(self):
        # Handle searching for headlines based on various criteria.
        params = {}
        print("\nHeadlines Menu:")
        print("1. Search by Keyword")
        print("2. Search by Category")
        print("3. Search by Country")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            params["q"] = input("Enter keyword: ")
        elif choice == "2":
            params["category"] = input("Enter category: ")
        elif choice == "3":
            params["country"] = input("Enter country: ")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
            return

        self.send_request("headlines", params)

        # Option selection with points
        self.select_option()

    def select_option(self):
        choice = input("Enter your choice (1-15): ")
        if choice.isdigit() and 1 <= int(choice) <= 15:
            self.points += 10  # Earn 10 points for each valid request
            data = {"option": int(choice), "info": f"Details for option {choice}"}
            self.client_socket.sendall(json.dumps(data).encode())
            print(f"Option {choice} selected. You earned 10 points!")
        else:
            print("Invalid choice. Please select a valid number.")

    def view_points(self):
        print(f"\nYour current points balance: {self.points} points.")

    def send_request(self, option, params):
        try:
            request = {"option": option, "params": params}
            self.client_socket.sendall(json.dumps(request).encode())
            response = self.client_socket.recv(4096).decode()
            response = json.loads(response)
            self.display_response(response)
        except (socket.error, json.JSONDecodeError) as e:
            print(f"Error: {e}")

    def list_sources(self):
        # Handle searching for headlines based on various criteria.
        params = {}
        print("\nHeadlines Menu:")
        print("1. Search by Keyword")
        print("2. Search by Category")
        print("3. Search by Country")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            params["q"] = input("Enter keyword: ")
        elif choice == "2":
            params["category"] = input("Enter category: ")
        elif choice == "3":
            params["country"] = input("Enter country: ")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
            return

        # Send the request and earn points for a valid action
        self.send_request("headlines", params)
        self.points += 10  # Award 10 points for making a headlines request
        print(f"You earned 10 points! Your current balance is {self.points} points.")

    def display_response(self, response):
        if isinstance(response, list):
            for item in response:
                print(f"- {item}")
        elif isinstance(response, dict):
            print(response.get("message", "No results found."))
        else:
            print("Unexpected response format.")

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12346
    NewsClient(HOST,PORT)
