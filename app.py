import tkinter as tk
from tkinter import ttk

APP_TITLE = "Dhaka Earthquake Helper"
APP_DESCRIPTION = (
    "After an earthquake, this tool shows which nearby hospitals have space, "
    "recommends the best one for your situation, and points you to the "
    "nearest open ground for safe assembly and gives various guidelines and history."
)

root = tk.Tk()
root.title(APP_TITLE)
root.geometry("900x600")

header = tk.Frame(root, bg="#f4f4f4")
header.pack(fill="x", padx=16, pady=(12, 4))
tk.Label(header, text=APP_TITLE, font=("Segoe UI", 15, "bold"),
         bg="#f4f4f4").pack(anchor="w")
tk.Label(header, text=APP_DESCRIPTION, wraplength=860, justify="left",
         fg="#444", bg="#f4f4f4").pack(anchor="w", pady=(2, 0))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=16, pady=12)

# Empty tabs for now. We will add them individually later.
notebook.add(tk.Frame(notebook), text="Locate")
notebook.add(tk.Frame(notebook), text="Guideline")
notebook.add(tk.Frame(notebook), text="Safe Grounds")
notebook.add(tk.Frame(notebook), text="History & Stats")

root.mainloop()