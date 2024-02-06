import os
from flask import Flask

port = int(os.environ.get("FLASK_APP_PORT", 8000))

app = Flask(__name__)

@app.route('/api/panels', methods=['GET'])
def panels():
    return {
        "panels": [
            {
                'name': 'Panel 1',
                'currentW': 200,
                'dayYieldW': 1000,
                'totalYieldW': 10000

            }
        ]
    }

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)