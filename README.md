Multithread News Client/Server Information System

Project Abstract:
In this project, we created a Multithreaded News Client Server Information System in python. 
The general purpose was to create a system which enables customer-side users to fetch and browse the latest news information which is made available by a server that sources this information from NewsAPI.org.
The server is able to use multiple threads to provide services to more than one client at the same time. There are a number of clients who connect to the server and make requests for specific news.
Clients make such requests and the server responds with availing news items of different categories such as headlines, sources and details. The client reformats these items to suit a user architecture.
This system focuses on client-server architecture, networking, and multithreading.

Course: ITCE320 - Network Programming
Term: Semester 1, 2024-2025
Instructor: Dr. Mohammed Almeer
Due Date: Saturday, December 7, 2024
------

Group Information:
Group Name: Network Programming Group 1
Course Code: ITCE320
Section: S1
Students:
Student 1: [shatha ebarahem ], [202103023]
Student 2: [Bayan isa ], [202202026]

--------

Table of Contents:
Requirements
How to Run
The Scripts
Additional Concepts
Acknowledgments
Conclusion

----------

Requirements:
The following dependencies and tools need to be installed in order to operate this project:

Python Libraries:
socket: Used for the creation of TCP connections.
requests: Used to get news information from the newsapi.org.
json: Used for the transmission of json data.

We have installed the required libraries by using the command:
“pip install requests”
--------------------
How to Run:
-Server:
Start the Server:
To start the server run the server script: “python server.py” >>> Server is now started and will check for connections from clients on port 12346.
Handling Client Requests:
The server is capable of providing three essential services: searching news headlines, listing sources and detailed information.
It provides services for several clients at the same time by making threads for each client connection.

-Client:
Connect to the Server: For this you need to run the client script and it will prompt you to enter a name, which you should do: “python client.py”

Main Menu Options:
Search Headlines: Have the capability to search and filter headlines by keyword, category, or country.
List Sources: Aid in the search for news sources based on Category, Country and Language.
Quit: Terminate the connection to the server.
-----------------------------------------------
The Scripts

1- Server Script:
The server script implements the following functionality:
Track connected clients: Monitors active clients through multithreading and processes requests made through them.
Access news source through NewsAPI: Makes requests to NewsAPI.org for obtaining new sources and stories.
Check formatting of user requests: Makes sure that the parameters in the requests are included before making the requests.

Key functions:
fetch_news_data ( endpoint : str , params : Dict[str, str] ): Calls the client address on the API for news and return response from the server.
validate_params(params): Validates the input parameters that clients fed the API.
handle_client(client_socket, client_address): Handles any communication with the respective client.
start_server(): Implements the server and waits for the clients to interact with the server.

2- Client Script:
The client script is designed to connect with the server, request for services and view the results.
Main Menu: Searching for headlines or sources of the news to fetch.
Response Handling: Represents the news headlines or sources based on the response of the server.
----------------------
Key functions:
search_headlines(): News headlines are searchable for the user.
list_sources(): News sources will be returned based on parameters asked in queries.
send_request(option, params): Sends a specific request to the server from the client.
display_response(response): The obtained response from the server is exhibited.
----------------------
Additional Concepts:
Multithreading: In order to allow the simultaneous connection of several clients, the server employs the threading module provided by Python.
Error Handling: The client and server scripts are able to cope with a number of errors thus providing the user with an experience without complications.
API Integration: The system provides connectivity to NewsAPI.org in order to receive certain news headlines and news sources as per the user’s discretion.
-------------------
Acknowledgments:
News API, which is Agence France Presse, provided the news data API.
Networked applications could be built with the assistance of Python.
Versioning and cooperative development were aided by GitHub.
------------------------
Conclusion
One of the goals of this project was to prove that it is possible to create a multithreaded client-server system interfaced with an
external API and networked with each other.The system is simple to understand, easy to grow,and firm enough to allow more than one
client at the same time.This project enabled the team to acquire practical knowledge about networking, multithreading and API integrations.
