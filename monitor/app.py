"""
HealthSync Internal Network Monitor Service
Internal network access only.
Deliberately contains command injection vulnerability.
"""
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "service": "HealthSync Network Monitor v1.0",
        "hostname": os.uname().nodename,
        "endpoints": ["/health", "/ping", "/diagnose"],
        "status": "running",
        "note": "Internal diagnostic service. Authorized personnel only."
    })


@app.route('/health')
def health():
    return jsonify({"status": "ok", "node": "monitor-internal"})


@app.route('/ping', methods=['GET'])
def ping():
    """
    Vulnerable endpoint: User input passed directly to shell.
    Example: GET /ping?host=8.8.8.8
    Command injection: GET /ping?host=8.8.8.8;id
    """
    host = request.args.get('host', '127.0.0.1')

    # UNSAFE: user input goes directly to os.popen()
    cmd = f"ping -c 2 {host} 2>&1"
    try:
        output = os.popen(cmd).read()
        return jsonify({
            "command": cmd,
            "output": output.strip()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/diagnose', methods=['GET'])
def diagnose():
    """
    Second vulnerable endpoint: network diagnostics.
    GET /diagnose?target=127.0.0.1
    """
    target = request.args.get('target', 'localhost')

    cmd = f"echo 'Diagnosing {target}...' && ping -c 1 {target} 2>&1 || echo 'Host unreachable'"
    try:
        output = os.popen(cmd).read()
        return jsonify({
            "target": target,
            "command": cmd,
            "output": output.strip()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/admin', methods=['GET'])
def admin():
    """
    Hidden admin panel — internal network only.
    """
    return jsonify({
        "message": "Admin panel — restricted to internal network",
        "hint": "System diagnostics available at /diagnose",
        "operator": "M. Vinter (last login: 2026-05-14 23:47)"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
