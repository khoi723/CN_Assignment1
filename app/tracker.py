import socket
import threading
import json
import os
import transform
import sys
import hashlib
import os
import bencodepy
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import urllib.parse
import subprocess
from urllib.request import urlopen
import re as r



class TrackerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        ip = get_local_ip()

        if path.startswith("/announce/upload"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            info_hash = query_params.get('info_hash', [None])[0]
            self._update_seeder(query_params.get('port', [None])[0], info_hash, ip)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"OK")
        elif path.startswith("/announce/download"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            info_hash = query_params.get('info_hash', [None])[0]
            response = self.find_and_print_line("tracker_directory/seeder_info.txt", info_hash)
            if response:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())  
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Not Found")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not Found")

    def _update_seeder(self, port, info_hash, ip):
        try:
            seeder_info = f"{ip}:{port}"
            file_dir = "tracker_directory"
            file_name = "seeder_info.txt"
            file_path = os.path.join(file_dir, file_name)
            os.makedirs(file_dir, exist_ok=True)  
            seeder_line = f"{info_hash}: {seeder_info}\n"

            if os.path.isfile(file_path):  
                with open(file_path, 'r') as file:
                    lines = file.readlines()
            else:
                lines = []

            seeder_exists = False
            for i, line in enumerate(lines):
                if info_hash in line:
                    seeder_ports = line.split(':')[1].strip().split(',')
                    if port in seeder_ports:
                        print(f"Port {port} already exists for {info_hash}. Skipping update.")
                        return
                    else:
                        seeder_exists = True
                        if line[-1] != '\n':
                            line += '\n'  
                        lines[i] = line.rstrip() + f", {seeder_info}\n"  
                        break

            if not seeder_exists:
                lines.append(seeder_line)

            with open(file_path, 'w') as file:
                file.writelines(lines)

            print(f"Seeder information updated for {file_name}.")
        except Exception as e:
            print(f"Error updating seeder information: {e}")
    
    def find_and_print_line(self, file_path, target_string):
        with open(file_path, 'r') as file:
            for line in file:
                if target_string + ": " in line:
                    return line.split(": ", 1)[1]  
                    break
        return None

def get_local_ip(interface='wlo1'):
    result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)

    ip_pattern = r'inet (\d+\.\d+\.\d+\.\d+)'
    match = re.search(ip_pattern, result.stdout)

    if match:
        return match.group(1)
    else:
        return None

def start_tracker(port=6880):
    server_address = (get_local_ip(), port)
    httpd = HTTPServer(server_address, TrackerRequestHandler)
    print(f"Tracker server is running on {get_local_ip()}:{port}")

    httpd.serve_forever()

start_tracker()

