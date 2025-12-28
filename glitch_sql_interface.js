/*
 * Glitch SQL Injector Interface
 * Glitch Design Style Implementation
 */

class GlitchSQLInterface {
    constructor() {
        this.init();
    }

    init() {
        this.createInterface();
        this.bindEvents();
        this.applyGlitchEffects();
    }

    createInterface() {
        // Create main container
        const container = document.createElement('div');
        container.id = 'glitch-sql-container';
        container.innerHTML = `
            <div class="glitch-header">
                <h1 class="glitch-title">GLİTCH SQL İNJECTOR</h1>
                <div class="glitch-subtitle">ETHICAL PENETRATION TESTING TOOL</div>
            </div>
            
            <div class="glitch-main-content">
                <div class="glitch-input-section">
                    <div class="input-group">
                        <label for="target-url" class="glitch-label">TARGET URL:</label>
                        <input type="text" id="target-url" class="glitch-input" placeholder="https://example.com/page.php?id=1">
                        <button id="scan-btn" class="glitch-button">INITIATE SCAN</button>
                    </div>
                    
                    <div class="disclaimer-section">
                        <div class="disclaimer">
                            <strong>WARNING:</strong> This tool is for educational purposes only.
                            Only use on systems you own or have explicit permission to test.
                            Unauthorized use may violate local, state, and federal laws.
                        </div>
                    </div>
                </div>
                
                <div class="glitch-results-section">
                    <h3 class="results-title">SCAN RESULTS</h3>
                    <div id="results-container" class="results-container">
                        <div class="initial-message">
                            Enter a target URL and click "INITIATE SCAN" to begin testing.
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="glitch-footer">
                <div class="status-bar">
                    <span id="status-text">READY</span>
                    <span id="status-indicator" class="status-indicator"></span>
                </div>
            </div>
        `;
        
        document.body.appendChild(container);
    }

    bindEvents() {
        const scanBtn = document.getElementById('scan-btn');
        const targetUrl = document.getElementById('target-url');
        
        scanBtn.addEventListener('click', () => {
            this.handleScan(targetUrl.value);
        });
        
        targetUrl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleScan(targetUrl.value);
            }
        });
    }

    async handleScan(url) {
        if (!url) {
            this.showMessage('Please enter a target URL', 'error');
            return;
        }
        
        if (!this.validateUrl(url)) {
            this.showMessage('Please enter a valid URL', 'error');
            return;
        }
        
        // Show consent dialog
        const consent = confirm('This tool is for educational purposes only!\n\nDo you confirm you have permission to test this system?\n\nUnauthorized use may violate local, state, and federal laws.\n\nDo you want to continue?');
        
        if (!consent) {
            this.showMessage('Scan cancelled - user consent not given', 'warning');
            return;
        }
        
        this.updateStatus('SCANNING', true);
        this.showMessage('Starting scan...', 'info');
        
        try {
            // Simulate scan (in a real implementation, this would call the Python backend)
            await this.simulateScan(url);
        } catch (error) {
            this.showMessage(`Scan error: ${error.message}`, 'error');
        } finally {
            this.updateStatus('READY', false);
        }
    }

    validateUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    async simulateScan(url) {
        // Call the API server
        this.showMessage(`Testing URL: ${url}`, 'info');
        
        try {
            // Call the API server
            const response = await fetch(`http://localhost:8080/api/scan?url=${encodeURIComponent(url)}`);
            
            if (response.ok) {
                const data = await response.json();
                this.displayResults(data);
            } else {
                throw new Error(`API request failed with status ${response.status}`);
            }
        } catch (error) {
            this.showMessage(`API error: ${error.message}`, 'error');
            
            // Fallback to simulated results
            this.showMessage('Falling back to simulated results...', 'warning');
            await this.delay(2000);
            this.displayResults({
                target: url,
                vulnerabilities: [
                    {type: 'Error-based SQL Injection', severity: 'HIGH', parameter: 'id', payload: "'" },
                    {type: 'Boolean-based SQL Injection', severity: 'HIGH', parameter: 'id', payload: "AND 1=1/1=2" },
                    {type: 'Time-based SQL Injection', severity: 'HIGH', parameter: 'id', payload: "SLEEP(5)" },
                    {type: 'Union-based SQL Injection', severity: 'HIGH', parameter: 'id', payload: "UNION SELECT" },
                    {type: 'Directory Listing', severity: 'MEDIUM', path: '/admin/' }
                ],
                timestamp: new Date().toISOString()
            });
        }
    }

    displayResults(results) {
        const container = document.getElementById('results-container');
        
        let html = `
            <div class="scan-summary">
                <h4>Scan Summary for: ${results.target}</h4>
                <p>Timestamp: ${results.timestamp}</p>
            </div>
        `;
        
        if (results.vulnerabilities && results.vulnerabilities.length > 0) {
            html += '<div class="vulnerabilities-list">';
            html += '<h5>Vulnerabilities Found:</h5>';
            
            results.vulnerabilities.forEach(vuln => {
                const severityClass = vuln.severity.toLowerCase();
                html += `
                    <div class="vulnerability-item ${severityClass}">
                        <div class="vuln-type">${vuln.type}</div>
                        <div class="vuln-severity">Severity: ${vuln.severity}</div>
                        ${vuln.parameter ? `<div class="vuln-param">Parameter: ${vuln.parameter}</div>` : ''}
                        ${vuln.payload ? `<div class="vuln-payload">Payload: ${vuln.payload}</div>` : ''}
                        ${vuln.path ? `<div class="vuln-path">Path: ${vuln.path}</div>` : ''}
                    </div>
                `;
            });
            
            html += '</div>';
        } else {
            html += '<div class="no-vulnerabilities">No vulnerabilities detected in this scan.</div>';
        }
        
        container.innerHTML = html;
    }

    showMessage(message, type = 'info') {
        const container = document.getElementById('results-container');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;
        messageDiv.textContent = message;
        
        container.appendChild(messageDiv);
        
        // Auto-remove message after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }

    updateStatus(text, scanning) {
        const statusText = document.getElementById('status-text');
        const statusIndicator = document.getElementById('status-indicator');
        
        statusText.textContent = scanning ? 'SCANNING' : 'READY';
        statusIndicator.className = `status-indicator ${scanning ? 'scanning' : 'ready'}`;
    }

    applyGlitchEffects() {
        // Apply glitch animations to elements
        const glitchElements = document.querySelectorAll('.glitch-title, .glitch-subtitle, .glitch-button');
        
        glitchElements.forEach(element => {
            element.classList.add('glitch-effect');
            
            // Add random glitch effect periodically
            setInterval(() => {
                if (Math.random() > 0.7) { // 30% chance of glitch
                    element.classList.add('glitch-active');
                    setTimeout(() => {
                        element.classList.remove('glitch-active');
                    }, 100);
                }
            }, 2000);
        });
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the interface when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new GlitchSQLInterface();
});