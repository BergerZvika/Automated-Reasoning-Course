#!/usr/bin/env python3
"""
PySMT Tutorial — execution server
Runs Python code sent from the browser and returns stdout/stderr.

Deploy to Render (free):
  1. Go to https://render.com  →  New Web Service
  2. Connect this GitHub repo
  3. Root Directory : pysmt
  4. Build Command  : pip install -r requirements.txt
  5. Start Command  : python server.py
  Then paste the Render URL into pysmt/index.html  (EXEC_URL constant).

Local usage:
  pip install -r pysmt/requirements.txt
  python pysmt/server.py
"""

import subprocess
import sys
import tempfile
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get('PORT', 5001))


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
    print(f'PySMT server running on port {PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=False)
