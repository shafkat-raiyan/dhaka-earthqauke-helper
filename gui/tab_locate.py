import tkinter as tk
from tkinter import ttk, messagebox
import json
import numpy as np
from functions.hospitals import Hospital
from functions.locator import EmergencyLocator

def load_locations():
    try:
        with open("data/locations.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Dhanmondi": [23.7461, 90.3742], "Mirpur": [23.8052, 90.3696]} 

def load_hospitals():
    try:
        with open("data/hospitals.json", "r") as f:
            data = json.load(f)
            hospital_list = []
            for h in data:
                
                name = h["name"]
                h_type = h["type"]
                loc = h["location"]
                count = h["patient_count"]
                
                if "coords" in h:
                    coords = h["coords"]
                else:
                    coords = None
                
                
                new_hospital = Hospital(name, h_type, loc, count, coords)
                hospital_list.append(new_hospital)
                
            return hospital_list
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def build_locate_tab(parent_frame, store):
    locations = load_locations()
    hospitals = load_hospitals()
    location_names = list(locations.keys())
    
    left_frame = tk.Frame(parent_frame, padx=10, pady=10)
    left_frame.pack(side="left", fill="y")
    
    right_frame = tk.Frame(parent_frame, padx=10, pady=10)
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(left_frame, text="Enter Emergency Details", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

    tk.Label(left_frame, text="Location:").grid(row=1, column=0, sticky="w", pady=10)
    combo_loc = ttk.Combobox(left_frame, values=location_names, state="readonly", width=18)
    combo_loc.grid(row=1, column=1, pady=10)

    tk.Label(left_frame, text="Age:").grid(row=2, column=0, sticky="w", pady=10)
    entry_age = tk.Entry(left_frame, width=20)
    entry_age.grid(row=2, column=1, pady=10)

    tk.Label(left_frame, text="Gender:").grid(row=3, column=0, sticky="w", pady=10)
    combo_gender = ttk.Combobox(left_frame, values=["Male", "Female", "Other"], state="readonly", width=18)
    combo_gender.grid(row=3, column=1, pady=10)

    tk.Label(left_frame, text="Injury Severity:").grid(row=4, column=0, sticky="w", pady=10)
    combo_severity = ttk.Combobox(left_frame, values=["Minor", "Moderate", "Severe"], state="readonly", width=18)
    combo_severity.grid(row=4, column=1, pady=10)



    locator = EmergencyLocator(hospitals, locations)

    def find_nearest_hospitals():
        loc_name = combo_loc.get()
        age = entry_age.get().strip()
        gender = combo_gender.get()
        severity = combo_severity.get()

        if not loc_name or not age or not gender or not severity:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a valid number.")
            return
            
        if int(age) < 1 or int(age) > 120:
            messagebox.showerror("Error", "Age must be a valid number between 1 and 120.")
            return

        top_3 = locator.get_nearest_hospitals(loc_name, count=3)
        if not top_3:
            messagebox.showerror("Error", "No hospital data is available.")
            return

       
        recommended_hospital = top_3[0][1].name
        store.add_log_entry({
            "location": loc_name,
            "age": int(age),
            "gender": gender,
            "priority": int(age) < 18 or gender == "Female",
            "severity": severity,
            "recommended_hospital": recommended_hospital,
        })

        result_text = f"Your Location: {loc_name}\n\nTop 3 Nearest Hospitals:\n\n"
        
        counter = 1
        for item in top_3:
            dist = item[0]
            h = item[1]
            
            dist_km = dist * 111.0
            
            result_text += f"{counter}. {h.name}\n"
            result_text += f"   Distance: ~{dist_km:.1f} km\n"
            result_text += f"   Type: {h.type} | Patients: {h.patient_count}\n\n"
            
            counter += 1

        display_area.config(state="normal")
        display_area.delete(1.0, tk.END)
        display_area.insert(tk.END, result_text)
        display_area.config(state="disabled")

    btn_locate = tk.Button(left_frame, text="Locate Nearest Help", bg="#007bff", fg="white", font=("Segoe UI", 10, "bold"), command=find_nearest_hospitals)
    btn_locate.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew")

    tk.Label(right_frame, text="Emergency Recommendations", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
    display_area = tk.Text(right_frame, font=("Segoe UI", 11), bg="#ffffff", relief="solid", bd=1, padx=10, pady=10)
    display_area.pack(fill="both", expand=True)
    display_area.insert(tk.END, "Enter your details on the left and click 'Locate Nearest Help'...")
    display_area.config(state="disabled")
