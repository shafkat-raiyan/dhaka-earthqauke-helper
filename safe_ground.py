class SafeGround:
    def __init__(self, ground_id, name, location, capacity):
        self.ground_id = str(ground_id).strip()
        self.name = str(name).strip()
        self.location = str(location).strip()
        self.capacity = int(capacity)

    def to_dict(self):
        # Useful for saving data later
        return {
            "id": self.ground_id,
            "name": self.name,
            "location": self.location,
            "capacity": self.capacity
        }