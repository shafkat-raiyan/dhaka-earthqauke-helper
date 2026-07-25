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



    def load_guideline_text(self):

        try:

            file = open(
                "guideline.txt",
                "r",
                encoding="utf-8"
            )

            text = file.read()

            file.close()

            return text


        except:

            return "Guideline file not found"




    def create_gui(self):

        title = tk.Label(
            self,
            text="Earthquake Guideline",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=10)



        guideline = self.load_guideline_text()


        tk.Label(
            self,
            text=guideline,
            justify="left",
            font=("Arial", 11)
        ).pack(anchor="w", padx=20)




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