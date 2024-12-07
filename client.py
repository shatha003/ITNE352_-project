import socket
import json

class NewsClient:
    def _init_(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_name = input("Enter your name: ")
        self.client_socket.sendall(self.client_name.encode())
        self.main_menu()

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Search Headlines")
            print("2. List Sources")
            print("3. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.search_headlines()
            elif choice == "2":
                self.list_sources()
            elif choice == "3":
                self.client_socket.sendall("quit".encode())
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    def search_headlines(self):
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
            params["country"] = input("Enter country code (e.g., 'us', 'ae'): ")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
            return

        self.send_request("headlines", params)

    def send_request(self, option, params):
        try:
            request = {"option": option, "params": params}
            self.client_socket.sendall(json.dumps(request).encode())
            response = self.client_socket.recv(8192).decode()
            response = json.loads(response)
            self.display_response(response)
        except (socket.error, json.JSONDecodeError) as e:
            print(f"Error: {e}")

    def display_response(self, response):
        if isinstance(response, list):
            if not response:
                print("No results found.")
                return

            print("\nSelect a headline to view details:")
            for idx, item in enumerate(response, 1):
                print(f"{idx}. {item['title']} (Source: {item['source_name']})")

            try:
                choice = int(input("\nEnter the number of the headline (1-15): ")) - 1
                if 0 <= choice < len(response):
                    self.display_headline_details(response[choice])
                else:
                    print("Invalid choice. Returning to menu.")
            except ValueError:
                print("Invalid input. Returning to menu.")
        else:
            print(response.get("message", "An error occurred."))

            #

    def display_headline_details(self, headline):
        print("\n--- Headline Details ---")
        print(f"Title: {headline['title']}")
        print(f"Source: {headline['source_name']}")
        print(f"Description: {headline.get('description', 'No description available.')}")
        print(f"URL: {headline.get('url', 'No URL available.')}")
        input("\nPress Enter to return to the main menu...")

    def list_sources(self):
        params = {}
        print("\nSources Menu:")
        print("1. Search by Category")
        print("2. Search by Country")
        print("3. Search by Language")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            params["category"] = input("Enter category: ")
        elif choice == "2":
            params["country"] = input("Enter country: ")
        elif choice == "3":
            params["language"] = input("Enter language: ")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
            return

        self.send_request("sources", params)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12346
    NewsClient(HOST,PORT)