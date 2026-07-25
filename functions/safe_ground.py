class SafeGround:
    def __init__(self, ground_id, name, location, capacity):
        self.ground_id = str(ground_id).strip()
        self.name = str(name).strip()
        self.location = str(location).strip()
        self.capacity = int(capacity)

    def to_dict(self):
    
        return {
            "id": self.ground_id,
            "name": self.name,
            "location": self.location,
            "capacity": self.capacity
        }

import json
import os

class SafeGroundManager:
    def __init__(self, filename="data/safegrounds.json"):
        self.filename = filename
        self.grounds = {}       
        self.used_ids = set() 
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return 
        
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for item in data:
                    sg = SafeGround(item['id'], item['name'], item['location'], item['capacity'])
                    self.grounds[sg.ground_id] = sg
                    self.used_ids.add(sg.ground_id)
        except (json.JSONDecodeError, KeyError):
            pass 

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump([g.to_dict() for g in self.grounds.values()], file, indent=4)

    def add_ground(self, ground_id, name, location, capacity):
        if ground_id in self.used_ids:
            raise ValueError("Duplicate ID found.")
        
        sg = SafeGround(ground_id, name, location, capacity)
        self.grounds[sg.ground_id] = sg
        self.used_ids.add(sg.ground_id)
        self.save_data()

    def delete_ground(self, ground_id):
        if ground_id in self.grounds:
            del self.grounds[ground_id]
            self.used_ids.remove(ground_id)
            self.save_data()
            return True
        return False