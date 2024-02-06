import os
from flask import Flask

port = int(os.environ.get("FLASK_APP_PORT", 8000))

app = Flask(__name__)

@app.route('/api/panels', methods=['GET'])
def panels():
    return {
        "panels": [
            {
                'id': 1,
                'name': 'Panel 1',
                'currentW': 200,
                'dayYieldW': 1000,
                'totalYieldW': 10000

            },
            {
                'id': 2,
                'name': 'Panel 2',
                'currentW': 250,
                'dayYieldW': 1400,
                'totalYieldW': 130000

            },
            {
                'id': 3,
                'name': 'Panel 3',
                'currentW': 150,
                'dayYieldW': 600,
                'totalYieldW': 7000
            }
        ]
    }

@app.route('/')
def index():
    return '<div><h3>ROUTES:</h3> <p>GET: <a href="/api/panels">/api/panels</a><p></div>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)