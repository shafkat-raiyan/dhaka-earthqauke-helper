import tkinter as tk
from tkinter import ttk

def build_locate_tab(parent_frame):
    
    tk.Label(parent_frame, text="Location:").grid(row=0, column=0, pady=10)
    entry_loc = tk.Entry(parent_frame)
    entry_loc.grid(row=0, column=1, pady=10)

    
    tk.Label(parent_frame, text="Age:").grid(row=1, column=0, pady=10)
    entry_age = tk.Entry(parent_frame)
    entry_age.grid(row=1, column=1, pady=10)

    
    tk.Label(parent_frame, text="Gender:").grid(row=2, column=0, pady=10)
    combo_gender = ttk.Combobox(parent_frame, values=["Male", "Female", "Other"])
    combo_gender.grid(row=2, column=1, pady=10)

    
    tk.Label(parent_frame, text="Injury Severity:").grid(row=3, column=0, pady=10)
    combo_severity = ttk.Combobox(parent_frame, values=["Minor", "Moderate", "Severe"])
    combo_severity.grid(row=3, column=1, pady=10)
