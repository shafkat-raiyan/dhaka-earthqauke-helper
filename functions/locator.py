import numpy as np

class EmergencyLocator:
    def __init__(self, hospitals, locations_dict):
        self.hospitals = hospitals
        self.locations = locations_dict

    def get_nearest_hospitals(self, loc_name, count=3):
        if loc_name not in self.locations:
            return []

        user_coords = np.array(self.locations[loc_name])
        hospital_distances = []

        i = 0
        for h in self.hospitals:
            h_coords = np.array(h.coords)
            dist = np.linalg.norm(user_coords - h_coords)
            
            hospital_distances.append( (dist, i, h) )
            i += 1

        hospital_distances.sort()
  
        top_hospitals = []
        for j in range(count):
            if j < len(hospital_distances):
                distance = hospital_distances[j][0]
                hospital_obj = hospital_distances[j][2]
                top_hospitals.append((distance, hospital_obj))

        return top_hospitals
