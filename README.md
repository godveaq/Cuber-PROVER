# Glitch SQL Injector

**Ethical SQL Injection Testing Tool for Educational Purposes**

## Description

Glitch SQL Injector is an advanced educational tool designed to help security professionals and students understand SQL injection vulnerabilities. This tool should only be used on systems you own or have explicit permission to test.

The tool features a terminal-style interface with glitch-themed aesthetics and provides comprehensive SQL injection testing capabilities using multiple methodologies including error-based, boolean-based, time-based, and union-based injection techniques.

## Features

- **Multiple SQL Injection Testing Techniques**:
  - Error-based SQL injection
  - Boolean-based blind SQL injection
  - Time-based blind SQL injection
  - Union-based SQL injection

- **Database Enumeration Capabilities**:
  - Extract database information (version, user, etc.)
  - Enumerate database tables
  - Enumerate table columns

- **Additional Security Testing**:
  - Directory listing vulnerability scanning

- **Terminal-Style Interface**:
  - Interactive command prompt
  - Color-coded output
  - Banner-style ASCII art logo
  - Glitch-themed design

- **Ethical Safeguards**:
  - Explicit consent required before each scan
  - Clear warnings about authorized use only
  - Legal disclaimers

## Installation Guide

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation Steps

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   # Or download and extract the ZIP file
   ```

2. **Navigate to the project directory**
   ```bash
   cd sql-map
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install requests
   ```

4. **Verify installation**
   ```bash
   python glitch_sql_injector.py --help
   ```

## Usage

### Interactive Mode (Recommended)

Run the tool without any arguments to enter interactive mode:

```bash
python glitch_sql_injector.py
```

In interactive mode, you can use the following commands:

- `scan <url>` - Scan a target URL for SQL injection vulnerabilities
  Example: `scan http://example.com/page.php?id=1`

- `help` - Show available commands and usage information

- `exit` or `quit` - Exit the tool

### Command Line Mode

Run the tool with a target URL directly:

```bash
python glitch_sql_injector.py "http://example.com/page.php?id=1"
```

### Output Options

You can save results to a file:

```bash
python glitch_sql_injector.py "http://example.com/page.php?id=1" -o results.txt
```

## Command Reference

### Available Commands in Interactive Mode

| Command | Description | Example |
|---------|-------------|---------|
| `scan <url>` | Test target URL for SQL injection vulnerabilities | `scan http://test.com/page.php?id=1` |
| `help` | Display help information | `help` |
| `exit` or `quit` | Exit the tool | `exit` |

### Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `url` | Target URL to test for SQL injection vulnerabilities | `python glitch_sql_injector.py "http://example.com?id=1"` |
| `--output`, `-o` | Output results to a file | `python glitch_sql_injector.py "http://example.com?id=1" -o results.txt` |

## Legal Disclaimer

**This tool is provided for educational and ethical testing purposes only.**

- Only use on systems you own or have explicit written permission to test
- Unauthorized use may violate local, state, and federal laws
- The authors are not responsible for any misuse of this tool
- Always ensure you have proper authorization before testing any system

## Configuration

The tool uses `config.json` for configuration. You can modify:

- Test payloads in the `test_payloads` array
- Error patterns to detect in the `error_patterns` array
- Common directories to scan in the `common_directories` array
- Request headers and timeouts in the `headers` and `timeout` settings

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'requests'**
   - Solution: Install the requests library with `pip install requests`

2. **Permission Denied Error**
   - Solution: Ensure you have read/write permissions in the project directory

3. **SSL Certificate Errors**
   - Solution: Add `--insecure` flag to your requests (if needed)

### Verifying Installation

To verify that the tool is installed correctly:

```bash
python glitch_sql_injector.py --help
```

You should see the help message with available options.

## Contributing

This tool is designed for educational purposes. If you find issues or have suggestions for improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Security Considerations

- This tool is designed to test for SQL injection vulnerabilities ethically
- Always have explicit written permission before testing systems
- Never use this tool against systems without authorization
- Be aware of legal implications in your jurisdiction

## Support

For educational purposes and questions about SQL injection concepts:

- Review the source code to understand the techniques
- Consult SQL injection prevention best practices
- Learn about secure coding practices

---

**Remember: Ethical use only! Only test systems you own or have explicit permission to test.**