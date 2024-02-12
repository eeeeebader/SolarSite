from pymongo import MongoClient, collection
from bson import ObjectId
from scraper import Scraper

from datetime import datetime

class MongoDocument:
    """
    A base class to represent a MongoDB document.
    """
    db = MongoClient('mongodb://localhost:27017/').panels
    collection_name = ''

    @classmethod
    def get_collection(cls) -> collection.Collection:
        """
        Retrieves the MongoDB collection for the model.
        """
        if not cls.collection_name:
            raise ValueError("collection_name is not set")
        return cls.db[cls.collection_name]

class Panel(MongoDocument):
    collection_name = 'panels'

    def __init__(self, serial_number, curYieldW, dailyYieldW, totalYieldW, dailyYieldsW=None, _id=None):
        self._id = _id or ObjectId()
        self.serial_number = serial_number
        self.curYieldW = curYieldW
        self.dailyYieldW = dailyYieldW
        self.dailyYieldsW = dailyYieldsW if dailyYieldsW is not None else []
        self.totalYieldW = totalYieldW

    def save(self):
        """
        Saves the document to MongoDB.
        """
        doc = self.to_dict()
        result = self.get_collection().update_one({'_id': self._id}, {'$set': doc}, upsert=True)
        return result

    def to_dict(self):
        """
        Converts the object to a dictionary suitable for MongoDB.
        """
        return {
            "_id": self._id,
            "serial_number": self.serial_number,
            "curYieldW": self.curYieldW,
            "dailyYieldW": self.dailyYieldW,
            "dailyYieldsW": self.dailyYieldsW,
            "totalYieldW": self.totalYieldW,
        }
    
    def update_values(self, data):
        """
        Updates the document with the given data.
        """
        print(data)
        print("test")
        self.serial_number = data['serial_number']
        self.curYieldW = data['currentW']
        self.dailyYieldW = data['dayYieldW']
        self.totalYieldW = data['totalYieldW']

        #check if the dailyYieldW is already in the list if not append. if update the value
        updated = False
        for dailyYieldW in self.dailyYieldsW:
            if dailyYieldW['date'] == datetime.now().strftime('%Y-%m-%d'):
                dailyYieldW['dayYieldW'] = data['dayYieldW']
                updated = True
            
        if not updated:
            self.dailyYieldsW.append({
                "date": datetime.now().strftime('%Y-%m-%d'),
                "dayYieldW": data['dayYieldW']
            })
        
        self.save()

    @classmethod
    def from_document(cls, document):
        if not document:
            return None
        return cls(
            _id=document.get('_id'),
            serial_number=document.get('serial_number'),
            curYieldW=document.get('curYieldW'),
            dailyYieldW=document.get('dailyYieldW'),
            totalYieldW=document.get('totalYieldW'),
            dailyYieldsW=document.get('dailyYieldsW', [])
        )


# Example usage
if __name__ == "__main__":
    panels = Scraper.get_all()
    for panel_json in panels:
        panel = Panel.get_collection().find_one({'serial_number': panel_json['serial_number']})
        if panel:
            panel = Panel.from_document(panel)
            panel.update_values(panel_json)
            continue

        panel = Panel(serial_number=panel_json['serial_number'], curYieldW=panel_json['currentW'], dailyYieldW=panel_json['dayYieldW'], totalYieldW=panel_json['totalYieldW'])
        panel.save()


    # Get panle by id and print it
    panel = Panel.get_collection().find_one({'serial_number': 1234398572})
    print(panel)


