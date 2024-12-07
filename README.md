 Multithreaded News Client/Server Information System

Project Abstract:
This project implements a **Multithreaded News Client-Server Information System** in Python. The system allows clients to request and view the latest news sourced from [NewsAPI.org](https://newsapi.org/). The server uses multithreading to handle multiple client connections simultaneously, providing services such as searching for news headlines, listing news sources, and retrieving detailed news. The system focuses on client-server architecture, networking, and multithreading.

Course: ITCE320 - Network Programming  
Term: Semester 1, 2024-2025  
Instructor: Dr. Mohammed Almeer  
Due Date: Saturday, December 7, 2024  

---

Group Information

**Group Name:** Network Programming Group 1  
**Course Code:** ITCE320  
**Section:** S1  
**Students:**  
- **Student 1:** Shatha Ebarahem [202103023]  
- **Student 2:** Bayan Isa [202202026]

---

Requirements
Python Libraries:
- socket: For TCP connections.
- requests: To fetch news data from [NewsAPI.org](https://newsapi.org/).
- json: To transmit JSON data.

To install the required libraries, run:
>>pip install requests<<


---
How to Run
Server:
Start the server by running the following command:

bash
Copy code
python server.py
The server will listen for incoming client connections on port 12346 and handle requests using multithreading.

Client:
Run the client script to connect to the server:

bash
Copy code
python client.py
The client will prompt for your name and then display a menu with options to:

Search Headlines: Filter news headlines by keyword, category, or country.
List Sources: View news sources based on parameters like category, country, and language.
Quit: Disconnect from the server.
The Scripts
Server Script:
The server handles client connections and fetches news from NewsAPI. Key functions include:

fetch_news_data(endpoint, params): Fetches news based on parameters.
validate_params(params): Validates the request parameters.
handle_client(client_socket, client_address): Manages communication with each client.
start_server(): Starts the server and listens for connections.
Client Script:
The client connects to the server and displays results. Key functions include:

search_headlines(): Searches for news headlines.
list_sources(): Lists available news sources.
send_request(option, params): Sends requests to the server.
display_response(response): Displays the server's response.
Additional Concepts
Multithreading: The server uses Python's threading module to handle multiple clients simultaneously.
Error Handling: Both client and server scripts handle errors to ensure smooth operation.
API Integration: The system integrates with NewsAPI.org to retrieve news.
Acknowledgments
NewsAPI: Provided the news data.
Python: Used for networking and multithreading.
GitHub: Used for version control and collaboration.
Conclusion
This project demonstrates the ability to create a multithreaded client-server system that interacts with an external API, providing real-time news data to clients. It enabled the team to gain practical experience in networking, multithreading, and API integration.
