#!/usr/bin/env python3
"""
PySMT Tutorial — local execution server
Runs Python code sent from the browser and returns stdout/stderr.

Usage:
    pip install pysmt z3-solver flask flask-cors
    pysmt-install --z3
    python server.py

The browser at pysmt/index.html will automatically connect to http://localhost:5001.
"""

import subprocess
import sys
import tempfile
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from the browser (file:// or any local origin)


@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json(silent=True) or {}
    code = data.get('code', '')
    if not code.strip():
        return jsonify({'stdout': '', 'stderr': '', 'returncode': 0})

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False,
                                     encoding='utf-8') as f:
        f.write(code)
        tmp = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp],
            capture_output=True, text=True, timeout=30
        )
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
        })
    except subprocess.TimeoutExpired:
        return jsonify({'stdout': '', 'stderr': 'Timeout (30 s)', 'returncode': 1})
    finally:
        os.unlink(tmp)


if __name__ == '__main__':
    print('PySMT local server running on http://localhost:5001')
    print('Press Ctrl+C to stop.')
    app.run(host='127.0.0.1', port=5001, debug=False)
