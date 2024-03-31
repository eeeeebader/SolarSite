import os
from pymongo import MongoClient, collection
from bson import ObjectId
from services.scraper import Scraper

from environments.environment import MONGO_DB_HOST, MONGO_DB_PORT, PANEL_UPDATE_INTERVAL_SECONDS

from datetime import datetime

class MongoDocument:
    """
    A base class to represent a MongoDB document.
    """
    mongoUrl = f"mongodb://{MONGO_DB_HOST}:{MONGO_DB_PORT}"
    db = MongoClient(mongoUrl).data
    collection_name = ''

    @classmethod
    def get_collection(cls) -> collection.Collection:
        """
        Retrieves the MongoDB collection for the model.
        """
        if not cls.collection_name:
            raise ValueError("collection_name is not set")
        return cls.db[cls.collection_name]
        
    @classmethod
    def get_all_panels(cls):
        """
        Retrieves all panel documents from the database and returns them as a list of Panel instances.
        """
        documents = cls.get_collection().find()  # Find all documents in the collection
        panels = [cls.from_document(doc) for doc in documents]  # Convert each document to a Panel instance
        return panels
    
    @classmethod
    def get_panel_by_id(cls, panel_id):
        """
        Retrieves a panel document by its ID from the database and returns it as a Panel instance.
        """
        document = cls.get_collection().find_one({'_id': ObjectId(panel_id)})  # Find the document by its ID
        return cls.from_document(document)  # Convert the document to a Panel instance
    
    @classmethod
    def get_panel_by_serial_number(cls, serial_number):
        """
        Retrieves a panel document by its serial number from the database and returns it as a Panel instance.
        """
        document = cls.get_collection().find_one({'serial_number': serial_number})
        return cls.from_document(document)

class Panel(MongoDocument):
    collection_name = 'panels'

    def __init__(self, serial_number, curYieldW, dailyYieldW, totalYieldW, dailyYieldsW=None, todaysYieldsW=None, _id=None):
        self._id = _id or ObjectId()
        self.serial_number = serial_number
        self.curYieldW = curYieldW
        self.dailyYieldW = dailyYieldW
        self.dailyYieldsW = dailyYieldsW if dailyYieldsW is not None else []
        self.totalYieldW = totalYieldW
        self.todaysYieldsW = todaysYieldsW if todaysYieldsW is not None else []

    def save(self):
        """
        Saves the document to MongoDB.
        """
        doc = self.to_dict(True)
        result = self.get_collection().update_one({'_id': self._id}, {'$set': doc}, upsert=True)
        return result

    def to_dict(self, include_object_id=False):
        """
        Converts the object to a dictionary suitable for MongoDB.
        """
        return {
            "_id": self._id if include_object_id else str(self._id),
            "serial_number": self.serial_number,
            "curYieldW": self.curYieldW,
            "dailyYieldW": self.dailyYieldW,
            "dailyYieldsW": self.dailyYieldsW,
            "totalYieldW": self.totalYieldW,
            "todaysYieldsW": self.todaysYieldsW
        }
    
    def set_inactive(self):
        """
        Sets the curYieldW value to 0 indicating that the panel is inactive.
        """
        self.curYieldW = 0
        self.save()
    
    def __interpolate_daily_yield(self, data):
        if(self.totalYieldW > 0):
            return data['totalYieldW'] - self.totalYieldW
        
        h_percent = (PANEL_UPDATE_INTERVAL_SECONDS / 100) / 60
        produced = data['curYieldW'] * h_percent

        return produced

    def update_values(self, data):
        """
        Updates the document with the given data.
        """
        self.curYieldW = data['curYieldW']

        updated = False
        for dailyYieldW in self.dailyYieldsW:
            if dailyYieldW['date'] == datetime.now().strftime('%Y-%m-%d'):
                dailyYieldW['yield'] = self.dailyYieldW + self.__interpolate_daily_yield(data)
                updated = True
            
        if not updated:
            self.dailyYieldsW.append({
                "date": datetime.now().strftime('%Y-%m-%d'),
                "yield": 0
            })
            
            self.todaysYieldsW=[]
            self.dailyYieldW = 0

        self.dailyYieldW += self.__interpolate_daily_yield(data)
        self.totalYieldW = data['totalYieldW']
            
        self.todaysYieldsW.append({
                "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "yield": self.curYieldW
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
            dailyYieldsW=document.get('dailyYieldsW', [
                {
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "yield": document.get('dailyYieldW')
                }
            ]),
            todaysYieldsW=document.get('todaysYieldsW', [
                {
                    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "yield": document.get('curYieldW')
                }
            ])
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

        panel = Panel(serial_number=panel_json['serial_number'], curYieldW=panel_json['curYieldW'], dailyYieldW=panel_json['dailyYieldW'], totalYieldW=panel_json['totalYieldW'])
        panel.save()


    # Get panle by id and print it
    panel = Panel.get_collection().find_one({'serial_number': 1234398572})
    print(panel)


