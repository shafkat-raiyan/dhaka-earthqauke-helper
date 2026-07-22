"""
storage.py
Owner: Member C

DataStore class: all file reading/writing for hospitals, grounds, and the
query log. Every read is wrapped so a missing or corrupted file never
crashes the app.
"""

import os
from .models import Hospital, Ground, DELIMITER


class DataStore:
    """Owns data.txt (hospitals + grounds) and query_log.txt (query history)."""

    def __init__(self, data_file="data/data.txt", log_file="data/query_log.txt"):
        self.data_file = data_file
        self.log_file = log_file
        self.hospitals = []   # list of Hospital objects
        self.grounds = []     # list of Ground objects
        self.log = []         # list of dict records (query history)

        self.load_data()
        self.load_log()

   

    def load_data(self):
        """Load hospital/ground data from a text file. Skips bad lines instead of crashing."""
        section = None
        seen_names = set()  

        try:
            with open(self.data_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []  

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("# HOSPITALS"):
                section = "hospitals"
                continue
            if line.startswith("# GROUNDS"):
                section = "grounds"
                continue

            try:
                if section == "hospitals":
                    hospital = Hospital.from_line(line)
                    if hospital.name in seen_names:
                        continue
                    seen_names.add(hospital.name)
                    self.hospitals.append(hospital)
                elif section == "grounds":
                    self.grounds.append(Ground.from_line(line))
            except (ValueError, IndexError):
                continue  

    def save_data(self):
        try:
            with open(self.data_file, "w") as f:
                f.write("# HOSPITALS\n")
                for h in self.hospitals:
                    f.write(h.to_line() + "\n")
                f.write("# GROUNDS\n")
                for g in self.grounds:
                    f.write(g.to_line() + "\n")
        except OSError:
            pass  

    

    def load_log(self):
        """Load past query history from a text file. Starts fresh if missing/corrupted."""
        if not os.path.exists(self.log_file):
            self.log = []
            return

        self.log = []
        try:
            with open(self.log_file, "r") as f:
                lines = f.readlines()
        except OSError:
            return

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            try:
                location, age, gender, priority, severity, recommended = line.split(DELIMITER)
                self.log.append({
                    "location": location,
                    "age": int(age),
                    "gender": gender,
                    "priority": priority == "True",
                    "severity": severity,
                    "recommended_hospital": recommended,
                })
            except (ValueError, IndexError):
                continue  

    def save_log(self):
        try:
            with open(self.log_file, "w") as f:
                for entry in self.log:
                    row = DELIMITER.join([
                        entry["location"], str(entry["age"]), entry["gender"],
                        str(entry["priority"]), entry["severity"],
                        str(entry["recommended_hospital"]),
                    ])
                    f.write(row + "\n")
        except OSError:
            pass 

    def add_log_entry(self, entry):
        self.log.append(entry)
        self.save_log()

   

    def export_summary(self, stats, path="session_summary.txt"):
        """Writes the current statistics to a plain text file the user can hand off."""
        try:
            with open(path, "w") as f:
                f.write("Dhaka Earthquake Helper - Session Summary\n")
                f.write("=" * 42 + "\n")
                if stats is None:
                    f.write("No queries logged yet.\n")
                    return True
                f.write(f"Total queries: {stats['total_queries']}\n")
                f.write(f"Average age: {stats['average_age']:.1f}\n")
                f.write(f"Youngest: {stats['youngest']:.0f}   Oldest: {stats['oldest']:.0f}\n")
                f.write(f"Priority (women/children) cases: {stats['priority_count']} "
                        f"({stats['priority_percent']:.0f}%)\n")
                sc = stats["severity_counts"]
                f.write(f"Severity - Minor: {sc['Minor']}  Moderate: {sc['Moderate']}  "
                        f"Severe: {sc['Severe']}\n")
            return True
        except OSError:
            return False

    def clear_log(self):
        """Clears all historical query logs from memory and the log file."""
        self.log = []
        self.save_log()

    def export_to_csv(self, stats, path):
        """Exports session summary statistics and all query logs to a CSV file."""
        import csv
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # Section 1: Summary Statistics
                writer.writerow(["Dhaka Earthquake Helper - Session Summary"])
                writer.writerow([])
                if stats:
                    writer.writerow(["Metric", "Value"])
                    writer.writerow(["Total Queries", stats["total_queries"]])
                    writer.writerow(["Average Age", f"{stats['average_age']:.1f}"])
                    writer.writerow(["Youngest Age", int(stats["youngest"])])
                    writer.writerow(["Oldest Age", int(stats["oldest"])])
                    writer.writerow(["Priority Cases Count", stats["priority_count"]])
                    writer.writerow(["Priority Cases %", f"{stats['priority_percent']:.1f}%"])
                    writer.writerow(["Severity - Minor", stats["severity_counts"]["Minor"]])
                    writer.writerow(["Severity - Moderate", stats["severity_counts"]["Moderate"]])
                    writer.writerow(["Severity - Severe", stats["severity_counts"]["Severe"]])
                else:
                    writer.writerow(["No queries logged yet."])
                
                writer.writerow([])
                writer.writerow([])
                
                # Section 2: Detailed Logs
                writer.writerow(["Detailed Query History"])
                writer.writerow(["Location", "Age", "Gender", "Priority Case", "Severity", "Recommended Hospital"])
                for entry in reversed(self.log):
                    writer.writerow([
                        entry["location"],
                        entry["age"],
                        entry["gender"],
                        "Yes" if entry["priority"] else "No",
                        entry["severity"],
                        entry["recommended_hospital"]
                    ])
            return True
        except OSError:
            return False

