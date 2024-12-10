import socket
import json

class NewsClient:
    def __init__(self, host, port):
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
            print("3. View Points")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.search_headlines()
            elif choice == "2":
                self.list_sources()
            elif choice == "3":
                self.view_points()
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
            params["category"] = input("Enter category (business, general, health, science, sports, technology): ")
        elif choice == "3":
            params["country"] = input("Enter country code (au, ca, jp, ae, sa, kr, us, ma): ")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
            return

        self.send_request("headlines", params)

    def list_sources(self):
        # Handle listing sources based on various criteria.
        params = {}
        print("\nSources Menu:")
        print("1. Search by Category")
        print("2. Search by Country")
        print("3. Search by Language")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            params["category"] = input("Enter category (business, general, health, science, sports, technology): ")
        elif choice == "2":
            params["country"] = input("Enter country code (au, ca, jp, ae, sa, kr, us, ma): ")
        elif choice == "3":
            params["language"] = input("Enter language (ar, en): ")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
            return

        self.send_request("sources", params)
        self.reward_points(5)  # Reward points for listing sources

    def view_points(self):
        # Display the user's current points.
        print(f"\nYour current points balance: {self.points} points.")

    def send_request(self, option, params):
        try:
            # Send the request to the server.
            request = {"option": option, "params": params}
            self.client_socket.sendall(json.dumps(request).encode())
            response = self.client_socket.recv(4096).decode()
            response = json.loads(response)
            self.display_response(option, response)
        except (socket.error, json.JSONDecodeError) as e:
            print(f"Error: {e}")

    def display_response(self, option, response):
        # Display the server's response based on its type.
        if isinstance(response, list) and response:
            if option == "headlines":
                for idx, item in enumerate(response, start=1):
                    print(f"{idx}. {item['title']} (Source: {item['source_name']})")
                choice = input("Enter your choice for more details or 'q' to go back: ")
                if choice.lower() != 'q' and choice.isdigit() and 1 <= int(choice) <= len(response):
                    self.display_headline_details(response[int(choice) - 1])
                self.reward_points(10)  # Reward points for viewing details
            elif option == "sources":
                for idx, item in enumerate(response, start=1):
                    print(f"{idx}. {item['source_name']}")
                choice = input("Enter your choice for more details or 'q' to go back: ")
                if choice.lower() != 'q' and choice.isdigit() and 1 <= int(choice) <= len(response):
                    self.display_source_details(response[int(choice) - 1])
        elif isinstance(response, dict):
            print(response.get("message", "No results found."))
        else:
            print("Unexpected response format or no data available.")

    def display_headline_details(self, headline):
        # Display detailed information about a selected headline.
        print("\n--- Headline Details ---")
        print(f"Title: {headline['title']}")
        print(f"Source: {headline['source_name']}")
        print(f"Description: {headline.get('description', 'No description available.')}")
        print(f"URL: {headline.get('url', 'No URL available.')}")
        input("\nPress Enter to return to the main menu...")
    
    def display_source_details(self, source):
        # Display detailed information about a selected source.
        print("\n--- Source Details ---")
        print(f"Name: {source['source_name']}")
        print(f"Description: {source.get('description', 'No description available.')}")
        print(f"URL: {source.get('url', 'No URL available.')}")
        input("\nPress Enter to return to the main menu...")

    def reward_points(self, points):
        # Add points to the user's balance and notify them.
        self.points += points
        print(f"You earned {points} points! Your current balance is {self.points} points.")

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12346
    NewsClient(HOST,PORT)