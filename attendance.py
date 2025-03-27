import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import sys
import csv

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        
        # Mac-specific optimizations
        if sys.platform == 'darwin':
            self.root.tk.call('tk', 'scaling', 2.0)
            self.font_small = ("Helvetica", 12)
            self.font_medium = ("Helvetica", 14)
            self.font_large = ("Helvetica", 18, "bold")
            self.min_width = 1200
            self.min_height = 700
        else:
            self.font_small = ("times new roman", 11)
            self.font_medium = ("times new roman", 13)
            self.font_large = ("times new roman", 20, "bold")
            self.min_width = 1100
            self.min_height = 650
            
        self.root.geometry(f"{self.min_width}x{self.min_height}")
        self.root.minsize(self.min_width, self.min_height)
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.var_attendance_id = tk.StringVar()
        self.var_student_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_department = tk.StringVar()
        self.var_time = tk.StringVar()
        self.var_date = tk.StringVar()
        self.var_attendance = tk.StringVar()
        self.var_search_by = tk.StringVar()
        self.var_search_txt = tk.StringVar()
        
        # Title
        title_lbl = tk.Label(self.root, text="ATTENDANCE MANAGEMENT SYSTEM", 
                           font=self.font_large, bg="#004d99", fg="white")
        title_lbl.pack(fill=tk.X)
        
        # Time
        def time():
            string = datetime.now().strftime('%H:%M:%S')
            self.clock_lbl.config(text=string)
            self.clock_lbl.after(1000, time)
            
        self.clock_lbl = tk.Label(self.root, font=self.font_small, 
                                bg="#004d99", fg="white")
        self.clock_lbl.place(relx=1.0, x=-120, y=5, width=100, height=25)
        time()
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bd=2, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(40, 10))
        
        # Left Frame (Attendance Details)
        left_frame = tk.LabelFrame(self.main_frame, bd=2, bg="white", relief=tk.RIDGE, 
                                 text="Attendance Details", font=self.font_medium)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inside Left Frame
        left_inside_frame = tk.Frame(left_frame, bd=2, relief=tk.RIDGE, bg="white")
        left_inside_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Labels and Entries
        # Attendance ID
        tk.Label(left_inside_frame, text="Attendance ID:", font=self.font_small, 
                bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(left_inside_frame, textvariable=self.var_attendance_id, 
                 font=self.font_small, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # Student ID
        tk.Label(left_inside_frame, text="Student ID:", font=self.font_small, 
                bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(left_inside_frame, textvariable=self.var_student_id, 
                 font=self.font_small, width=20).grid(row=0, column=3, padx=5, pady=5)
        
        # Name
        tk.Label(left_inside_frame, text="Name:", font=self.font_small, 
                bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(left_inside_frame, textvariable=self.var_name, 
                 font=self.font_small, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Department
        tk.Label(left_inside_frame, text="Department:", font=self.font_small, 
                bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(left_inside_frame, textvariable=self.var_department, 
                 font=self.font_small, width=20).grid(row=1, column=3, padx=5, pady=5)
        
        # Time
        tk.Label(left_inside_frame, text="Time:", font=self.font_small, 
                bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(left_inside_frame, textvariable=self.var_time, 
                 font=self.font_small, width=20).grid(row=2, column=1, padx=5, pady=5)
        
        # Date
        tk.Label(left_inside_frame, text="Date:", font=self.font_small, 
                bg="white").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(left_inside_frame, textvariable=self.var_date, 
                 font=self.font_small, width=20).grid(row=2, column=3, padx=5, pady=5)
        
        # Attendance Status
        tk.Label(left_inside_frame, text="Status:", font=self.font_small, 
                bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.attendance_combo = ttk.Combobox(left_inside_frame, textvariable=self.var_attendance, 
                                            font=self.font_small, width=18, state="readonly")
        self.attendance_combo["values"] = ("Present", "Absent")
        self.attendance_combo.current(0)
        self.attendance_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(left_inside_frame, bd=2, relief=tk.RIDGE, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="ew")
        
        btn_save = tk.Button(btn_frame, text="Save", command=self.add_data, 
                            width=15, font=self.font_small, bg="#004d99", fg="white")
        btn_save.grid(row=0, column=0, padx=2, pady=5)
        
        btn_update = tk.Button(btn_frame, text="Update", command=self.update_data, 
                              width=15, font=self.font_small, bg="#004d99", fg="white")
        btn_update.grid(row=0, column=1, padx=2, pady=5)
        
        btn_delete = tk.Button(btn_frame, text="Delete", command=self.delete_data, 
                              width=15, font=self.font_small, bg="#004d99", fg="white")
        btn_delete.grid(row=0, column=2, padx=2, pady=5)
        
        btn_reset = tk.Button(btn_frame, text="Reset", command=self.reset_data, 
                             width=15, font=self.font_small, bg="#004d99", fg="white")
        btn_reset.grid(row=0, column=3, padx=2, pady=5)
        
        # Export CSV Button
        btn_export = tk.Button(left_inside_frame, text="Export CSV", command=self.export_to_csv, 
                              width=15, font=self.font_small, bg="#004d99", fg="white")
        btn_export.grid(row=5, column=0, columnspan=4, pady=5, sticky="ew")
        
        # Configure grid weights for responsive layout
        for i in range(4):
            left_inside_frame.grid_columnconfigure(i, weight=1)
        
        # Right Frame (Attendance Records)
        right_frame = tk.LabelFrame(self.main_frame, bd=2, bg="white", relief=tk.RIDGE, 
                                  text="Attendance Records", font=self.font_medium)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search Frame
        search_frame = tk.LabelFrame(right_frame, bd=2, bg="white", relief=tk.RIDGE, 
                                   text="Search", font=self.font_medium)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search Components
        tk.Label(search_frame, text="Search By:", font=self.font_small, 
                bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        combo_search = ttk.Combobox(search_frame, textvariable=self.var_search_by, 
                                   font=self.font_small, state="readonly", width=15)
        combo_search["values"] = ("ID", "Student ID", "Name", "Department")
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=5, pady=5)
        
        txt_search = ttk.Entry(search_frame, textvariable=self.var_search_txt, 
                              font=self.font_small, width=15)
        txt_search.grid(row=0, column=2, padx=5, pady=5)
        
        btn_search = tk.Button(search_frame, text="Search", command=self.search_data, 
                              width=10, font=self.font_small, bg="#004d99", fg="white")
        btn_search.grid(row=0, column=3, padx=5, pady=5)
        
        btn_show_all = tk.Button(search_frame, text="Show All", command=self.fetch_data, 
                                width=10, font=self.font_small, bg="#004d99", fg="white")
        btn_show_all.grid(row=0, column=4, padx=5, pady=5)
        
        # Configure search frame grid weights
        for i in range(5):
            search_frame.grid_columnconfigure(i, weight=1)
        
        # Table Frame
        table_frame = tk.Frame(right_frame, bd=2, bg="white", relief=tk.RIDGE)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Attendance Table
        self.attendance_table = ttk.Treeview(table_frame, columns=("id", "student_id", "name", "department", "time", "date", "attendance"),
                                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)
        
        # Configure columns
        self.attendance_table.heading("id", text="Attendance ID")
        self.attendance_table.heading("student_id", text="Student ID")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("department", text="Department")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("attendance", text="Status")
        
        self.attendance_table["show"] = "headings"
        
        # Set column widths
        self.attendance_table.column("id", width=100, anchor=tk.CENTER)
        self.attendance_table.column("student_id", width=80, anchor=tk.CENTER)
        self.attendance_table.column("name", width=120, anchor=tk.CENTER)
        self.attendance_table.column("department", width=120, anchor=tk.CENTER)
        self.attendance_table.column("time", width=80, anchor=tk.CENTER)
        self.attendance_table.column("date", width=80, anchor=tk.CENTER)
        self.attendance_table.column("attendance", width=80, anchor=tk.CENTER)
        
        self.attendance_table.pack(fill=tk.BOTH, expand=1)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)
        
        # Create database and table
        self.create_db()
        self.fetch_data()

    # Database Methods
    def create_db(self):
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id TEXT PRIMARY KEY,
                    student_id TEXT,
                    name TEXT,
                    department TEXT,
                    time TEXT,
                    date TEXT,
                    attendance TEXT)''')
        conn.commit()
        conn.close()

    def add_data(self):
        if self.var_attendance_id.get() == "" or self.var_student_id.get() == "":
            messagebox.showerror("Error", "ID and Student ID fields are required", parent=self.root)
        else:
            try:
                # First check if student exists in student database
                student_conn = sqlite3.connect("student_small.db")
                student_cursor = student_conn.cursor()
                student_cursor.execute("SELECT id FROM student WHERE id=?", (self.var_student_id.get(),))
                student_exists = student_cursor.fetchone() is not None
                student_conn.close()
                
                if not student_exists:
                    messagebox.showerror("Error", f"Student ID {self.var_student_id.get()} not found in student database", parent=self.root)
                    return
                    
                # Then proceed with attendance record check
                conn = sqlite3.connect("attendance.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM attendance WHERE id=?", (self.var_attendance_id.get(),))
                row = cursor.fetchone()
                
                if row:
                    messagebox.showerror("Error", f"ID {self.var_attendance_id.get()} already exists", parent=self.root)
                else:
                    cursor.execute("INSERT INTO attendance VALUES (?,?,?,?,?,?,?)", (
                        self.var_attendance_id.get(),
                        self.var_student_id.get(),
                        self.var_name.get(),
                        self.var_department.get(),
                        self.var_time.get(),
                        self.var_date.get(),
                        self.var_attendance.get()
                    ))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Record added successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM attendance")
        data = cursor.fetchall()
        
        self.attendance_table.delete(*self.attendance_table.get_children())
        for i in data:
            self.attendance_table.insert("", tk.END, values=i)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.attendance_table.focus()
        content = self.attendance_table.item(cursor_row)
        data = content["values"]
        
        if data:
            self.var_attendance_id.set(data[0])
            self.var_student_id.set(data[1])
            self.var_name.set(data[2])
            self.var_department.set(data[3])
            self.var_time.set(data[4])
            self.var_date.set(data[5])
            self.var_attendance.set(data[6])

    def update_data(self):
        if self.var_attendance_id.get() == "":
            messagebox.showerror("Error", "ID is required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect("attendance.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE attendance SET student_id=?, name=?, department=?, time=?, date=?, attendance=? WHERE id=?", (
                    self.var_student_id.get(),
                    self.var_name.get(),
                    self.var_department.get(),
                    self.var_time.get(),
                    self.var_date.get(),
                    self.var_attendance.get(),
                    self.var_attendance_id.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Record updated successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_attendance_id.get() == "":
            messagebox.showerror("Error", "ID is required", parent=self.root)
        else:
            try:
                if messagebox.askyesno("Delete", "Delete this record?", parent=self.root):
                    conn = sqlite3.connect("attendance.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM attendance WHERE id=?", (self.var_attendance_id.get(),))
                    conn.commit()
                    conn.close()
                    self.fetch_data()
                    self.reset_data()
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_attendance_id.set("")
        self.var_student_id.set("")
        self.var_name.set("")
        self.var_department.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attendance.set("Present")

    def search_data(self):
        if self.var_search_by.get() == "" or self.var_search_txt.get() == "":
            messagebox.showerror("Error", "Select search option and enter value", parent=self.root)
        else:
            try:
                conn = sqlite3.connect("attendance.db")
                cursor = conn.cursor()
                
                if self.var_search_by.get() == "ID":
                    cursor.execute("SELECT * FROM attendance WHERE id LIKE ?", 
                                  ('%' + self.var_search_txt.get() + '%',))
                elif self.var_search_by.get() == "Student ID":
                    cursor.execute("SELECT * FROM attendance WHERE student_id LIKE ?", 
                                  ('%' + self.var_search_txt.get() + '%',))
                elif self.var_search_by.get() == "Name":
                    cursor.execute("SELECT * FROM attendance WHERE name LIKE ?", 
                                  ('%' + self.var_search_txt.get() + '%',))
                elif self.var_search_by.get() == "Department":
                    cursor.execute("SELECT * FROM attendance WHERE department LIKE ?", 
                                  ('%' + self.var_search_txt.get() + '%',))
                
                data = cursor.fetchall()
                
                if len(data) != 0:
                    self.attendance_table.delete(*self.attendance_table.get_children())
                    for i in data:
                        self.attendance_table.insert("", tk.END, values=i)
                else:
                    messagebox.showinfo("Info", "No matching records found", parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def export_to_csv(self):
        try:
            # Ask user where to save the file with priyank.csv as default name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save attendance data as",
                initialfile="priyank.csv"  # Set default filename
            )
            
            if not file_path:  # User cancelled the save dialog
                return
                
            conn = sqlite3.connect("attendance.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance")
            data = cursor.fetchall()
            conn.close()
            
            # Write data to CSV file
            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                # Write header
                csvwriter.writerow(['Attendance ID', 'Student ID', 'Name', 'Department', 'Time', 'Date', 'Status'])
                # Write data
                csvwriter.writerows(data)
            
            messagebox.showinfo("Success", f"Data exported successfully to:\n{file_path}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error exporting data: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    obj = Attendance(root)
    root.mainloop()