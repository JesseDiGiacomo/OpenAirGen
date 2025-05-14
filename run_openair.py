from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/run_openair', methods=['POST'])
def run_openair():
    try:
        processo = subprocess.run(
            ['python3', 'run_all.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            text=True
        )
        logs = processo.stdout.splitlines() + processo.stderr.splitlines()
        return jsonify({'status': 'ok', 'logs': logs})
    except Exception as e:
        return jsonify({'status': 'erro', 'logs': [str(e)]}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)