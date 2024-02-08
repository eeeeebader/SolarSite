import os
import random
from flask import Flask, request, jsonify
from datetime import datetime, timedelta


port = int(os.environ.get("FLASK_APP_PORT", 8000))

app = Flask(__name__)

@app.route('/api/panels/<int:panel_id>', methods=['GET'])
def get_panel_data(panel_id):
    from_date_str = request.args.get('from_date', '')  # Expected format 'YYYY-MM-DD'
    to_date_str = request.args.get('to_date', '')  # Expected format 'YYYY-MM-DD'

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use 'YYYY-MM-DD'."}), 400
    
    obj = {
        "id": panel_id,
        "name": f"Panel {panel_id}",
        "dailyYieldsW": []
    }
    
    cur_date = from_date
    for i in range((to_date - from_date).days + 1):
        obj["dailyYieldsW"].append({
            "date": cur_date.strftime('%Y-%m-%d'),
            "dayYieldW": random.randint(0, 600)
        })
        cur_date += timedelta(days=1)

    return jsonify(obj)

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
    return '<div><h3>ROUTES:</h3> <p>GET: <a href="/api/panels">/api/panels</a></p><p>GET: <a href="/api/panels/1?from_date=2024-01-01&to_date=2024-02-01">/api/panels/:id?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD</a></p></div>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)