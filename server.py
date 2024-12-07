import socket  
import threading 
import requests  
import json  

# Server configuration
HOST = "127.0.0.1"  
PORT = 12346        
API_KEY = "43edc4ea317f4f048115f3287c4789fb"  
MAX_CLIENTS = 3 

VALID_LANGUAGES = {"en", "ar"}
VALID_COUNTRIES = {"au", "ca", "jp", "ae", "sa", "kr", "us", "ma"}
VALID_CATEGORIES = {"business", "general", "health", "science", "sports", "technology"}

# fetch data from NewsAPI
def fetch_news_data(endpoint, params):
   
    url = f"https://newsapi.org/v2/{endpoint}"
    headers = {"Authorization": API_KEY}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # if failed, raise error
        return response.json()  # return JSON response
    except requests.RequestException as e:
        print(f"[ERROR] API Request Failed: {e}")
        return {"status": "error", "message": str(e)}

def validate_params(params):
    errors = []
    if "language" in params and params["language"] not in VALID_LANGUAGES:
        errors.append(f"Invalid language: {params['language']} (Allowed: en, ar)")
    if "country" in params and params["country"] not in VALID_COUNTRIES:
        errors.append(f"Invalid country: {params['country']} (Allowed: au, ca, jp, ae, sa, kr, us, ma)")
    if "category" in params and params["category"] not in VALID_CATEGORIES:
        errors.append(f"Invalid category: {params['category']} (Allowed: business, general, health, science, sports, technology)")
    return errors


# handle client connection
def handle_client(client_socket, client_address):
   
    try:
        client_name = client_socket.recv(1024).decode()  # Receive client name
        print(f"[INFO] Connected to {client_name} from {client_address}")

        while True:
            request_data = client_socket.recv(1024).decode()  # Receive request
            if not request_data or request_data.lower() == "quit":
                print(f"[INFO] {client_name} disconnected.")
                break

            # parse the request and fetch data
            request = json.loads(request_data)
            option = request.get("option")
            params = request.get("params", {})
            print(f"[INFO] {client_name} requested {option} with params: {params}")

            # Validate parameters
            validation_errors = validate_params(params)
            if validation_errors:
                response = {"status": "error", "message": "; ".join(validation_errors)}
                client_socket.send(json.dumps(response).encode())
                continue


            # choose endpoint based on request
            if option == "headlines":
                endpoint = "top-headlines"
            elif option == "sources":
                endpoint = "sources"
            else:
                response = {"status": "error", "message": "Invalid option"}
                client_socket.send(json.dumps(response).encode())
                continue

             # Choose endpoint based on request
            endpoint = "top-headlines" if option == "headlines" else "sources" if option == "sources" else None
            if not endpoint:
                response = {"status": "error", "message": "Invalid option"}
                client_socket.send(json.dumps(response).encode())
                continue

            # get data from NewsAPI
            api_response = fetch_news_data(endpoint, params)

            # save response to a JSON file for testing
            with open(f"{client_name}_{option}.json", "w") as file:
                json.dump(api_response, file, indent=4)

            # prepare response to send to the client
            if api_response.get("status") == "ok":
                if option == "headlines":
                    response = [{"source_name": article["source"]["name"], "title": article["title"]} for article in api_response.get("articles", [])[:15]]
                elif option == "sources":
                    response = [{"source_name": source["name"]} for source in api_response.get("sources", [])[:15]]
            else:
                response = {"status": "error", "message": api_response.get("message", "Error fetching data")}

            # Send the response back to the client
            client_socket.send(json.dumps(response).encode())

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
    finally:
        client_socket.close()

# start server and listen for client connections
def start_server():
   
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    print(f"[INFO] Server running on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()  # accept new client
            print(f"[INFO] New connection from {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()  # start a thread for each client
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down.")
    finally:
        server_socket.close()

# run the server
if __name__ == "__main__":
    start_server()
