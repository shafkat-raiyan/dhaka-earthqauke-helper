class Hospital:
    def __init__(self, name, hospital_type, location, patient_count, coords=None):
        self.name = name
        self.type = hospital_type
        self.location = location
        self.patient_count = int(patient_count)
        self.coords = coords if coords else [0.0, 0.0]

    def display_info(self):
        """Returns a formatted string of the hospital's information."""
        return f" {self.name} | Type: {self.type} | Location: {self.location} | Patients: {self.patient_count}"
