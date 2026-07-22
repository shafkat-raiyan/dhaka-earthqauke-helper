"""
tab_history.py
Owner: Member C

History & Statistics tab: shows past queries and aggregate stats.
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk

from constants import FONT_BOLD


class HistoryTab(tk.Frame):
    def __init__(self, parent, store, locator):
        super().__init__(parent, bg="#f4f4f4", padx=16, pady=16)
        self.store = store
        self.locator = locator
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        top = tk.Frame(self, bg="#f4f4f4")
        top.pack(fill="x")
        tk.Label(top, text="Query History", font=FONT_BOLD, bg="#f4f4f4").pack(side="left")
        tk.Button(top, text="Export Summary", command=self.on_export).pack(side="right")
        tk.Button(top, text="Clear History", command=self.on_clear, bg="#d9534f", fg="white").pack(side="right", padx=(0, 6))

        # Filter bar
        filter_bar = tk.Frame(self, bg="#f4f4f4")
        filter_bar.pack(fill="x", pady=(4, 8))

        tk.Label(filter_bar, text="Search Location:", bg="#f4f4f4").pack(side="left", padx=(0, 4))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(filter_bar, textvariable=self.search_var, width=12)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh())

        tk.Label(filter_bar, text="Severity:", bg="#f4f4f4").pack(side="left", padx=(0, 4))
        self.filter_severity_var = tk.StringVar(value="All")
        self.severity_combo = ttk.Combobox(
            filter_bar, textvariable=self.filter_severity_var,
            values=["All", "Minor", "Moderate", "Severe"],
            state="readonly", width=9
        )
        self.severity_combo.pack(side="left", padx=(0, 10))
        self.severity_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Label(filter_bar, text="Priority:", bg="#f4f4f4").pack(side="left", padx=(0, 4))
        self.filter_priority_var = tk.StringVar(value="All")
        self.priority_combo = ttk.Combobox(
            filter_bar, textvariable=self.filter_priority_var,
            values=["All", "Priority Only", "Standard Only"],
            state="readonly", width=12
        )
        self.priority_combo.pack(side="left")
        self.priority_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        self.listbox = tk.Listbox(self, font=("Segoe UI", 10))
        self.listbox.pack(fill="both", expand=True, pady=(6, 10))

        tk.Label(self, text="Statistics", font=FONT_BOLD, bg="#f4f4f4").pack(anchor="w")
        self.stats_label = tk.Label(self, text="", bg="#fff", justify="left",
                                     padx=10, pady=10, highlightbackground="#ccc",
                                     highlightthickness=1, anchor="w")
        self.stats_label.pack(fill="x", pady=4)

        self.export_status = tk.Label(self, text="", bg="#f4f4f4", fg="#2a7")
        self.export_status.pack(anchor="w")

    def refresh(self):
        self.listbox.delete(0, tk.END)
        
        search_query = self.search_var.get().strip().lower()
        sev_filter = self.filter_severity_var.get()
        pri_filter = self.filter_priority_var.get()
        
        filtered_entries = []
        for entry in self.store.log:
            # 1. Location search filter
            if search_query and search_query not in entry["location"].lower():
                continue
            # 2. Severity filter
            if sev_filter != "All" and entry["severity"] != sev_filter:
                continue
            # 3. Priority filter
            if pri_filter == "Priority Only" and not entry["priority"]:
                continue
            if pri_filter == "Standard Only" and entry["priority"]:
                continue
            filtered_entries.append(entry)

        if not filtered_entries:
            if not self.store.log:
                self.listbox.insert(tk.END, "No queries logged yet.")
            else:
                self.listbox.insert(tk.END, "No matching queries found.")
        else:
            for entry in reversed(filtered_entries):
                flag = " [PRIORITY]" if entry["priority"] else ""
                line = (f"{entry['location']} | Age {entry['age']} | {entry['gender']}{flag} | "
                        f"{entry['severity']} -> {entry['recommended_hospital']}")
                self.listbox.insert(tk.END, line)

        stats = self.locator.get_statistics()
        if not stats:
            self.stats_label.config(text="No statistics yet - run a Locate search first.")
            return
        sc = stats["severity_counts"]
        text = (
            f"Total queries: {stats['total_queries']}\n"
            f"Average age: {stats['average_age']:.1f}   "
            f"Youngest: {stats['youngest']:.0f}   Oldest: {stats['oldest']:.0f}\n"
            f"Priority (women/children): {stats['priority_count']} "
            f"({stats['priority_percent']:.0f}%)\n"
            f"Severity - Minor: {sc['Minor']}  Moderate: {sc['Moderate']}  "
            f"Severe: {sc['Severe']}"
        )
        self.stats_label.config(text=text)

    def on_export(self):
        stats = self.locator.get_statistics()
        if not stats:
            messagebox.showinfo("Nothing to Export", "No queries logged yet. Run a Locate search first.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files (Excel)", "*.csv"), ("Text Files", "*.txt")],
            title="Export Session Summary"
        )
        if not filepath:
            return

        if filepath.endswith(".csv"):
            ok = self.store.export_to_csv(stats, filepath)
        else:
            ok = self.store.export_summary(stats, filepath)

        if ok:
            import os
            filename = os.path.basename(filepath)
            self.export_status.config(text=f"Saved to {filename}", fg="#2a7")
        else:
            self.export_status.config(text="Could not save file.", fg="#c00")
            messagebox.showerror("Export Failed", "Could not write the export file.")

    def on_clear(self):
        if not self.store.log:
            messagebox.showinfo("Clear History", "Query history is already empty.")
            return
        if messagebox.askyesno("Clear History", "Are you sure you want to permanently clear all query logs?"):
            self.store.clear_log()
            self.refresh()
            self.export_status.config(text="Query history cleared.", fg="#d9534f")



if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from functions.storage import DataStore
    from functions.locator import EmergencyLocator

    root = tk.Tk()
    root.title("tab_history.py standalone test")
    root.geometry("560x420")

    store = DataStore()
    locator = EmergencyLocator(store)

    store.add_log_entry({"location": "Mirpur 10", "age": 8, "gender": "Female",
                          "priority": True, "severity": "Severe",
                          "recommended_hospital": "Test Hospital"})
    store.add_log_entry({"location": "Dhanmondi 27", "age": 45, "gender": "Male",
                          "priority": False, "severity": "Minor",
                          "recommended_hospital": "Test Hospital 2"})

    HistoryTab(root, store, locator).pack(fill="both", expand=True)
    root.mainloop()
