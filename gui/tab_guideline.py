import tkinter as tk
from tkinter import messagebox

from functions.guideline import Guideline

class GuidelineTab(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.data = Guideline()

        self.water = tk.IntVar()
        self.firstaid = tk.IntVar()
        self.flashlight = tk.IntVar()
        self.food = tk.IntVar()

        self.create_gui()

    def create_gui(self):

        title = tk.Label(
            self,
            text="Earthquake Guideline",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=10)

        guideline = """
Before Earthquake
• Prepare emergency kit
• Keep emergency numbers

During Earthquake
• Drop, Cover and Hold
• Stay away from windows

After Earthquake
• Go to safe open ground
• Help injured people
"""

        tk.Label(
            self,
            text=guideline,
            justify="left"
        ).pack()

        tk.Label(
            self,
            text="Emergency Checklist",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Checkbutton(
            self,
            text="Water",
            variable=self.water
        ).pack(anchor="w")

        tk.Checkbutton(
            self,
            text="First Aid Kit",
            variable=self.firstaid
        ).pack(anchor="w")

        tk.Checkbutton(
            self,
            text="Flashlight",
            variable=self.flashlight
        ).pack(anchor="w")

        tk.Checkbutton(
            self,
            text="Emergency Food",
            variable=self.food
        ).pack(anchor="w")

        tk.Button(
            self,
            text="Save Checklist",
            command=self.save
        ).pack(pady=5)

        tk.Button(
            self,
            text="Show Statistics",
            command=self.show_stats
        ).pack()

    def save(self):

        self.data.items.clear()

        self.data.add_item(
            "Water",
            self.water.get()
        )

        self.data.add_item(
            "First Aid Kit",
            self.firstaid.get()
        )

        self.data.add_item(
            "Flashlight",
            self.flashlight.get()
        )

        self.data.add_item(
            "Emergency Food",
            self.food.get()
        )

        self.data.save()

        messagebox.showinfo(
            "Done",
            "Checklist Saved"
        )

    def show_stats(self):

        self.data.load()

        total, ready, percent = self.data.statistics()

        messagebox.showinfo(

            "Statistics",

            "Total Item : " + str(total) +
            "\nReady Item : " + str(ready) +
            "\nPrepared : " + str(round(percent, 2)) + "%"

        )

