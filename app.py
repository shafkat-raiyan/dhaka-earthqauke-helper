import tkinter as tk
from tkinter import ttk

from functions.safe_ground import SafeGroundManager
from gui.tab_safegrounds import build_safe_grounds_tab
from gui.tab_locate import build_locate_tab
from functions.storage import DataStore
from gui.tab_history import HistoryTab, EmergencyLocator

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


locate_frame = tk.Frame(notebook)
notebook.add(locate_frame, text="Locate")
build_locate_tab(locate_frame)

guideline_frame = GuidelineTab(notebook)
notebook.add(guideline_frame, text="Guideline")

manager = SafeGroundManager() 
store = DataStore()
locator = EmergencyLocator(store)

safe_grounds_frame = tk.Frame(notebook)
notebook.add(safe_grounds_frame, text="Safe Grounds")
build_safe_grounds_tab(safe_grounds_frame, manager) 

history_frame = HistoryTab(notebook, store, locator)
notebook.add(history_frame, text="History & Stats")

root.mainloop()