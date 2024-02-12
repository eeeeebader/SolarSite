import os
from flask import Flask, request, jsonify
from datetime import datetime
import sched, time

from services.mongo_controller import Panel
from services.scraper import Scraper

port = int(os.environ.get("FLASK_APP_PORT", 8000))
app = Flask(__name__)

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

    return jsonify(res)

@app.route('/')
def index():
    return '<div><h3>ROUTES:</h3> <p>GET: <a href="/api/panels">/api/panels</a></p><p>GET: <a href="/api/panels/65ca6cde853f3e03bc318fa6?from_date=2024-01-01&to_date=2024-02-01">/api/panels/:id?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD</a></p></div>'


def update_panels(scheduler):
    scheduler.enter(520, 1, update_panels, (scheduler,))
    panels = Scraper.get_all()

    db_panels = Panel.get_all_panels()
    for db_panel in db_panels:
        found = False
        for panel in panels:
            if db_panel.serial_number == panel['serial_number']:
                found = True
                break
        if not found:
            db_panel.set_inactive()

    for panel_json in panels:
        panel = Panel.get_collection().find_one({'serial_number': panel_json['serial_number']})
        if panel:
            panel.update_values(panel_json)
        else:
            panel = Panel.from_document(panel_json)
            panel.save()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

    panels_scheduler = sched.scheduler(time.time, time.sleep)
    panels_scheduler.enter(1, 1, update_panels, (panels_scheduler,))
    panels_scheduler.run()
    print("panels update scheduler started")

