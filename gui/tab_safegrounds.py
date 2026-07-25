import tkinter as tk
from tkinter import ttk, messagebox, filedialog  # এখানে filedialog যুক্ত করা হয়েছে

# ==========================================
# সাধারণ ইউজারদের জন্য (Find Safe Grounds)
# ==========================================
def build_find_grounds_tab(parent_frame, manager):
    search_frame = tk.Frame(parent_frame, padx=10, pady=10)
    search_frame.pack(fill="x")
    
    tk.Label(search_frame, text="Search (Name or Location):").pack(side="left", padx=5)
    search_var = tk.StringVar()
    entry_search = tk.Entry(search_frame, textvariable=search_var, width=30)
    entry_search.pack(side="left", padx=5)

    tree = ttk.Treeview(parent_frame, columns=("ID", "Name", "Location", "Capacity"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Location", text="Location")
    tree.heading("Capacity", text="Capacity")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_list(query=""):
        for row in tree.get_children():
            tree.delete(row)
        for sg in manager.grounds.values():
            if query.lower() in sg.name.lower() or query.lower() in sg.location.lower():
                tree.insert("", "end", values=(sg.ground_id, sg.name, sg.location, sg.capacity))

    def search_data():
        refresh_list(search_var.get().strip())
        
    def reset_search():
        search_var.set("")
        refresh_list()

    # --- এক্সপোর্ট করার নতুন ফাংশন ---
    def export_list():
        # চেক করা হচ্ছে টেবিলে কোনো ডেটা আছে কিনা
        children = tree.get_children()
        if not children:
            messagebox.showwarning("Warning", "The list is empty. Nothing to export.")
            return
        
        # ইউজার কোথায় ফাইল সেভ করতে চায় তার ডায়লগ বক্স
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Safe Grounds List",
            initialfile="Safe_Grounds_List.txt"
        )
        
        if not filepath:
            return  # ইউজার সেভ না করে ক্যানসেল করে দিলে ফিরে আসবে
            
        try:
            # File Handling: .txt ফাইলে ডেটা রাইট (Write) করা হচ্ছে
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("Dhaka Earthquake Helper - Safe Grounds List\n")
                f.write("=" * 50 + "\n")
                
                # টেবিলের বর্তমান ডেটাগুলো ফাইলে লেখা
                for row_id in children:
                    item = tree.item(row_id)
                    values = item['values']
                    f.write(f"Ground Name : {values[1]}\n")
                    f.write(f"Location    : {values[2]}\n")
                    f.write(f"Capacity    : {values[3]} people\n")
                    f.write("-" * 30 + "\n")
                    
            messagebox.showinfo("Success", "Safe grounds list exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    # বাটনগুলো যুক্ত করা
    tk.Button(search_frame, text="Search", command=search_data, bg="#cce5ff", width=10).pack(side="left", padx=5)
    tk.Button(search_frame, text="Reset", command=reset_search, bg="#e2e3e5", width=10).pack(side="left", padx=5)
    
    # নতুন Export List বাটন
    tk.Button(search_frame, text="Export List", command=export_list, bg="#d4edda", width=15).pack(side="left", padx=20)
    
    refresh_list()


# ==========================================
# অ্যাডমিন/ম্যানেজারদের জন্য (Manage Data)
# ==========================================
def build_manage_grounds_tab(parent_frame, manager):
    input_frame = tk.Frame(parent_frame, padx=10, pady=10)
    input_frame.pack(fill="x")

    tk.Label(input_frame, text="ID:").grid(row=0, column=0, sticky="w")
    entry_id = tk.Entry(input_frame)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Name:").grid(row=0, column=2, sticky="w")
    entry_name = tk.Entry(input_frame)
    entry_name.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(input_frame, text="Location:").grid(row=1, column=0, sticky="w")
    entry_loc = tk.Entry(input_frame)
    entry_loc.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Capacity:").grid(row=1, column=2, sticky="w")
    entry_cap = tk.Entry(input_frame)
    entry_cap.grid(row=1, column=3, padx=5, pady=5)

    tree = ttk.Treeview(parent_frame, columns=("ID", "Name", "Location", "Capacity"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Location", text="Location")
    tree.heading("Capacity", text="Capacity")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_list():
        for row in tree.get_children():
            tree.delete(row)
        for sg in manager.grounds.values():
            tree.insert("", "end", values=(sg.ground_id, sg.name, sg.location, sg.capacity))

    def add_entry():
        try:
            g_id = entry_id.get().strip()
            name = entry_name.get().strip()
            loc = entry_loc.get().strip()
            cap = int(entry_cap.get().strip())

            if not g_id or not name or not loc:
                messagebox.showerror("Error", "Fields cannot be empty.")
                return
            if cap < 0:
                messagebox.showerror("Error", "Capacity cannot be negative.")
                return

            manager.add_ground(g_id, name, loc, cap)
            refresh_list()
            
            entry_id.delete(0, tk.END)
            entry_name.delete(0, tk.END)
            entry_loc.delete(0, tk.END)
            entry_cap.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Safe ground added!")
        except ValueError as e:
            if "Duplicate" in str(e):
                messagebox.showerror("Error", "This ID already exists.")
            else:
                messagebox.showerror("Error", "Capacity must be a valid positive number.")

    def delete_entry():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row from the table to delete.")
            return
        
        item = tree.item(selected[0])
        g_id = str(item['values'][0])
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete ID: {g_id}?"):
            if manager.delete_ground(g_id):
                refresh_list()
                messagebox.showinfo("Success", "Safe ground deleted successfully!")
            else:
                messagebox.showerror("Error", "Could not delete the record.")

    btn_frame = tk.Frame(input_frame)
    btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
    
    tk.Button(btn_frame, text="Add Ground", command=add_entry, bg="#d4edda", width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Delete Selected", command=delete_entry, bg="#f8d7da", width=15).pack(side="left", padx=10)

    refresh_list()