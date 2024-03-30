from services.mongo_controller import Panel
from services.scraper import Scraper

import datetime

def update_panels() -> bool:
    panels = Scraper.get_all()
    serial_numbers_db = [panel.serial_number for panel in Panel.get_all_panels()]
    serial_numbers_scraper = [panel["serial_number"] for panel in panels]

    inactive_serial_numbers = [i for i in serial_numbers_db if i not in serial_numbers_scraper]

    for serial_number in inactive_serial_numbers:
        panel = Panel.get_panel_by_serial_number(serial_number)
        panel.set_inactive()

    for panel_json in panels:
        panel = Panel.get_collection().find_one({'serial_number': panel_json['serial_number']})
        if panel:
            panel = Panel.from_document(panel)
            panel.update_values(panel_json)
            continue

        panel = Panel.from_document(panel_json)
        panel.save()

    return len(panels) > 0

if __name__ == "__main__":
    updated = update_panels()
    if updated:
        print(f"Updated panels at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Update failed at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")