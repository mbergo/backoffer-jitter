import os
import sys
import time
import json
import requests
import datetime
import argparse
import threading
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, quote_plus
from requests.exceptions import ConnectionError


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("Hello World", "utf8"))
        return
        
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("Hello World", "utf8"))
            return
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("Hello World", "utf8"))
            return

def run():
    print('starting server...')
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print('running server...')
    httpd.serve_forever()

class OCC:
    def __init__(self, url, token, headers, data):
        self.url = url
        self.token = token
        self.headers = headers
        self.data = data
        self.backoff = 0
        self.occ = 0
        self.occ_max = 5
        self.occ_sleep = 0.5
        self.occ_sleep_max = 5
        self.occ_sleep_increment = 0.5
        self.occ_sleep_increment_max = 5
        
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data)
            if response.status_code == 200:
                self.occ = 0
                self.backoff = 0
                self.occ_sleep = 0.5
                self.occ_sleep_increment = 0.5
                return True
            elif response.status_code == 429:
                self.occ += 1
                if self.occ >= self.occ_max:
                    self.occ = 0
                    self.backoff += 1
                    if self.backoff >= 1:
                        self.backoff = 0
                        self.occ_sleep += self.occ_sleep_increment
                        if self.occ_sleep >= self.occ_sleep_max:
                            self.occ_sleep = 0.5
                            self.occ_sleep_increment += self.occ_sleep_increment_increment
        finally:
            time.sleep(self.occ_sleep)
            return False
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    