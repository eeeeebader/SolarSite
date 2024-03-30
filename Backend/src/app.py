import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from datetime import datetime

from services.mongo_controller import Panel

port = int(os.environ.get("FLASK_APP_PORT", 8000))
app = Flask(__name__)
CORS(app, support_credentials=True)

PANEL_UPDATE_INTERVAL = int(os.environ.get('PANEL_UPDATE_INTERVAL_SECONDS', 300))
DEBUG_FLAG = os.environ.get('DEBUG', 'false').lower() == 'true'

@app.route('/api/panels/<panel_id>', methods=['GET'])
def get_panel_data(panel_id):
    from_date_str = request.args.get('from_date', '') 
    to_date_str = request.args.get('to_date', '') 

    panel = Panel.get_panel_by_id(panel_id)
    if not panel:
        return jsonify({"error": "Panel not found."}), 404
    res = panel.to_dict()
    
    if from_date_str == '' or to_date_str == '':
        return jsonify(res)

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use 'YYYY-MM-DD'."}), 400
    
    if from_date > to_date:
        return jsonify({"error": "The 'from_date' must be before the 'to_date'."}), 400
    
    res['dailyYieldsW'] = [d for d in res['dailyYieldsW'] if from_date <= datetime.strptime(d['date'], '%Y-%m-%d') <= to_date]
    return jsonify(res)

@app.route('/api/panels', methods=['GET'])
def panels():
    res = []
    panles = Panel.get_all_panels()

    for panel in panles:
        res.append(panel.to_dict())

        # remove the dailyYieldsW and todaysYieldsW from the response
        res[-1].pop('dailyYieldsW', None)
        res[-1].pop('todaysYieldsW', None)

    return jsonify(res)

@app.route('/')
def index():
    return '<div><h3>ROUTES:</h3> <p>GET: <a href="/api/panels">/api/panels</a></p><p>GET: <a href="/api/panels/65ca6cde853f3e03bc318fa6?from_date=2024-01-01&to_date=2024-02-01">/api/panels/:id?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD</a></p></div>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=DEBUG_FLAG)


