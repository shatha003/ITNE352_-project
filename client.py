import socket
import json
import requests
from rich.console import Console

class NewsClient:
    def __init__(self, host, port):
        #Initialize the client, connect to the server and set up the necessary variables.