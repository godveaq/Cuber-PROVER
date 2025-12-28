# Glitch SQL Injector - File Structure

This document outlines all files created for the Glitch SQL Injector tool.

## Core Application Files
- `glitch_sql_injector.py` - Main Python application for SQL injection testing
- `api_server.py` - API server to handle requests from the web interface
- `config.json` - Configuration file for the tool
- `requirements.txt` - Python dependencies

## Web Interface Files
- `index.html` - Main HTML page with glitch styling
- `glitch_sql_interface.js` - JavaScript for the frontend interface
- `glitch_sql_interface.js` - Contains the glitch design elements

## Launch Scripts
- `glitch_sql.bat` - Windows batch script to run the tool from command line
- `start_glitch_sql.bat` - Windows batch script to start the API server and web interface

## Documentation
- `README.md` - Main documentation file with usage instructions

## Features
1. Command-line interface for direct usage
2. Web-based interface with glitch design aesthetics
3. Configurable testing parameters
4. Ethical usage warnings and confirmations
5. Vulnerability scanning capabilities
6. Directory listing detection

## Usage Instructions
### Command Line
```bash
python glitch_sql_injector.py "http://example.com/page.php?id=1"
```

### Web Interface
1. Start the API server: `python api_server.py`
2. Open `index.html` in your browser, or use the start script
3. Enter the target URL and click "INITIATE SCAN"

### Batch Script (Windows)
```bash
start_glitch_sql.bat
```

## Legal Notice
This tool is designed for educational purposes only. Only use on systems you own or have explicit permission to test. Unauthorized use may violate local, state, and federal laws.