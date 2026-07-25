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
BEFORE EARTHQUAKE

• Prepare emergency kit
• Keep important documents safe
• Save emergency contact numbers


DURING EARTHQUAKE

• Drop, Cover and Hold
• Stay away from windows
• Do not use elevators


AFTER EARTHQUAKE

• Check injuries
• Move to open safe areas
• Help injured people


EMERGENCY KIT

• Water
• First Aid Kit
• Flashlight
• Emergency Food
"""



        text_box = tk.Text(
            self,
            height=13,
            width=70,
            font=("Arial", 11),
            wrap="word"
        )

        text_box.insert(
            "1.0",
            guideline
        )

        text_box.config(
            state="disabled"
        )

        text_box.pack(
            padx=20,
            pady=5
        )



        tk.Label(
            self,
            text="Emergency Checklist",
            font=("Arial", 12, "bold")
        ).pack(pady=5)




        tk.Checkbutton(
            self,
            text="Water",
            variable=self.water
        ).pack(anchor="w", padx=20)



        tk.Checkbutton(
            self,
            text="First Aid Kit",
            variable=self.firstaid
        ).pack(anchor="w", padx=20)



        tk.Checkbutton(
            self,
            text="Flashlight",
            variable=self.flashlight
        ).pack(anchor="w", padx=20)



        tk.Checkbutton(
            self,
            text="Emergency Food",
            variable=self.food
        ).pack(anchor="w", padx=20)



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


        checked_items = ""


        for item in self.data.items:

            if item["status"] == 1:

                checked_items += "✓ " + item["name"] + "\n"



        if checked_items == "":

            checked_items = "No item prepared"



        messagebox.showinfo(

            "Statistics",

            "Total Item : " + str(total) +
            "\nReady Item : " + str(ready) +
            "\nPrepared : " + str(round(percent, 2)) +
            "%\n\nPrepared Items:\n" +
            checked_items

        )