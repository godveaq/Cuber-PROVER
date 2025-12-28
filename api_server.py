#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Glitch SQL Injector API Server
===============================
Simple API server to handle requests from the web interface
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import subprocess
import threading
import time

class GlitchSQLAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve the main HTML page
            self.serve_file('../index.html', 'text/html')
        elif parsed_path.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status_data = {
                'status': 'running',
                'tool': 'Glitch SQL Injector',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(status_data).encode())
        elif parsed_path.path.startswith('/api/scan'):
            # Parse query parameters
            params = parse_qs(parsed_path.query)
            target_url = params.get('url', [None])[0]
            
            if not target_url:
                self.send_error(400, 'Missing target URL')
                return
            
            # In a real implementation, this would call the scanner
            # For now, we'll simulate the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Simulate scan results
            results = {
                'target': target_url,
                'status': 'completed',
                'vulnerabilities': [
                    {
                        'type': 'SQL Injection',
                        'severity': 'HIGH',
                        'parameter': 'id',
                        'payload': "'",
                        'description': 'Potential SQL injection vulnerability detected'
                    }
                ],
                'timestamp': time.time()
            }
            self.wfile.write(json.dumps(results).encode())
        else:
            # Try to serve static files
            if parsed_path.path.startswith('/glitch_sql_interface.js'):
                self.serve_file('../glitch_sql_interface.js', 'application/javascript')
            else:
                self.send_error(404, 'File not found')
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/scan':
            try:
                request_data = json.loads(post_data.decode('utf-8'))
                target_url = request_data.get('url')
                
                if not target_url:
                    self.send_error(400, 'Missing target URL')
                    return
                
                # In a real implementation, this would call the scanner
                # For now, we'll simulate the response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Simulate scan results
                results = {
                    'target': target_url,
                    'status': 'completed',
                    'vulnerabilities': [
                        {
                            'type': 'Error-based SQL Injection',
                            'severity': 'HIGH',
                            'parameter': 'id',
                            'payload': "'",
                            'description': 'Potential error-based SQL injection vulnerability detected'
                        },
                        {
                            'type': 'Boolean-based SQL Injection',
                            'severity': 'HIGH',
                            'parameter': 'id',
                            'payload': "AND 1=1/1=2",
                            'description': 'Potential boolean-based SQL injection vulnerability detected'
                        },
                        {
                            'type': 'Time-based SQL Injection',
                            'severity': 'HIGH',
                            'parameter': 'id',
                            'payload': "SLEEP(5)",
                            'description': 'Potential time-based SQL injection vulnerability detected'
                        },
                        {
                            'type': 'Union-based SQL Injection',
                            'severity': 'HIGH',
                            'parameter': 'id',
                            'payload': "UNION SELECT",
                            'description': 'Potential union-based SQL injection vulnerability detected'
                        }
                    ],
                    'timestamp': time.time()
                }
                self.wfile.write(json.dumps(results).encode())
            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON data')
        else:
            self.send_error(404, 'Endpoint not found')
    
    def serve_file(self, file_path, content_type):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_error(404, 'File not found')

def run_server(port=8080):
    """Run the API server"""
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, GlitchSQLAPIHandler)
    print(f"Glitch SQL Injector API server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    print("Starting Glitch SQL Injector API Server...")
    print("Warning: This tool is for educational purposes only.")
    print("Only use on systems you own or have explicit permission to test.")
    print("Unauthorized use may violate local, state, and federal laws.\n")
    
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)