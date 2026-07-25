class Hospital:
    def __init__(self, name, hospital_type, location, patient_count, max_capacity=0, coords=None):
        self.name = name
        self.type = hospital_type
        self.location = location
        self.patient_count = int(patient_count)
        self.max_capacity = int(max_capacity)
        self.coords = coords if coords else [0.0, 0.0]

    def get_capacity_percent(self):
        if self.max_capacity == 0:
            return 0.0
        return (self.patient_count / self.max_capacity) * 100

    def display_info(self):
        """Returns a formatted string of the hospital's information."""
        return f" {self.name} | Type: {self.type} | Location: {self.location} | Capacity: {self.get_capacity_percent():.0f}%"
