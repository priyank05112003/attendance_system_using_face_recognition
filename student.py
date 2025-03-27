import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import cv2
import os
from PIL import Image, ImageTk

def migrate_database():
    """Migrate database to ensure photo column exists"""
    conn = sqlite3.connect("student_small.db")
    cursor = conn.cursor()

    try:
        # Check if photo column exists, if not, add it
        cursor.execute("PRAGMA table_info(student)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'photo' not in columns:
            cursor.execute("ALTER TABLE student ADD COLUMN photo TEXT DEFAULT 'No'")
            conn.commit()
            print("Photo column added successfully!")
    except sqlite3.OperationalError as e:
        print(f"Database migration error: {e}")
    except Exception as e:
        print(f"Unexpected error during migration: {e}")
    finally:
        conn.close()

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("900x600+0+0")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.var_dep = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_year = tk.StringVar()
        self.var_semester = tk.StringVar()
        self.var_std_id = tk.StringVar()
        self.var_div = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_name = tk.StringVar() 
        self.var_search_by = tk.StringVar()
        self.var_search_txt = tk.StringVar()
        self.var_radio1 = tk.StringVar()
        
        # Title
        title_lbl = tk.Label(self.root, text="STUDENT MANAGEMENT", font=("times new roman", 20, "bold"), bg="#004d99", fg="white")
        title_lbl.pack(fill=tk.X)
        
        # Time
        def time():
            string = datetime.now().strftime('%H:%M:%S')
            self.clock_lbl.config(text=string)
            self.clock_lbl.after(1000, time)
            
        self.clock_lbl = tk.Label(self.root, font=("times new roman", 10), bg="#004d99", fg="white")
        self.clock_lbl.place(x=800, y=5, width=90, height=20)
        time()
        
        # Back button
        back_btn = tk.Button(self.root, text="Back", command=self.root.destroy, width=5, font=("times new roman", 10), bg="#004d99", fg="white")
        back_btn.place(x=10, y=5, width=50, height=20)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bd=2, bg="white")
        main_frame.place(x=5, y=35, width=890, height=560)
        
        # Left Frame (Course & Student Info)
        left_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE, text="Student Info", font=("times new roman", 10, "bold"))
        left_frame.place(x=5, y=5, width=350, height=545)
        
        # Course Information
        course_frame = tk.LabelFrame(left_frame, bd=2, bg="white", relief=tk.RIDGE, text="Course", font=("times new roman", 10, "bold"))
        course_frame.place(x=5, y=5, width=335, height=120)
        
        # Department & Course (row 0)
        tk.Label(course_frame, text="Department:", font=("times new roman", 10), bg="white").grid(row=0, column=0, padx=2, pady=2)
        ttk.Combobox(course_frame, textvariable=self.var_dep, font=("times new roman", 10), state="readonly", width=10,
                      values=("CS", "IT", "Civil", "Mech")).grid(row=0, column=1, padx=2, pady=2)
        
        tk.Label(course_frame, text="Course:", font=("times new roman", 10), bg="white").grid(row=0, column=2, padx=2, pady=2)
        ttk.Combobox(course_frame, textvariable=self.var_course, font=("times new roman", 10), state="readonly", width=10,
                      values=("BSc", "BTech", "MTech", "MCA")).grid(row=0, column=3, padx=2, pady=2)
        
        # Year & Semester (row 1)
        tk.Label(course_frame, text="Year:", font=("times new roman", 10), bg="white").grid(row=1, column=0, padx=2, pady=2)
        ttk.Combobox(course_frame, textvariable=self.var_year, font=("times new roman", 10), state="readonly", width=10,
                      values=("2022-23", "2023-24", "2024-25")).grid(row=1, column=1, padx=2, pady=2)
        
        tk.Label(course_frame, text="Semester:", font=("times new roman", 10), bg="white").grid(row=1, column=2, padx=2, pady=2)
        ttk.Combobox(course_frame, textvariable=self.var_semester, font=("times new roman", 10), state="readonly", width=10,
                      values=("1", "2", "3", "4", "5", "6")).grid(row=1, column=3, padx=2, pady=2)
        
        # Student Details
        student_frame = tk.LabelFrame(left_frame, bd=2, bg="white", relief=tk.RIDGE, text="Student Details", font=("times new roman", 10, "bold"))
        student_frame.place(x=5, y=130, width=335, height=350)
        
        # Student ID & Division (row 0)
        tk.Label(student_frame, text="Student ID:", font=("times new roman", 10), bg="white").grid(row=0, column=0, padx=2, pady=2)
        ttk.Entry(student_frame, textvariable=self.var_std_id, font=("times new roman", 10), width=15).grid(row=0, column=1, padx=2, pady=2)
        
        tk.Label(student_frame, text="Division:", font=("times new roman", 10), bg="white").grid(row=0, column=2, padx=2, pady=2)
        ttk.Combobox(student_frame, textvariable=self.var_div, font=("times new roman", 10), state="readonly", width=8,
                      values=("A", "B", "C", "D")).grid(row=0, column=3, padx=2, pady=2)
    
        # Gender & Phone (row 1)
        tk.Label(student_frame, text="Gender:", font=("times new roman", 10), bg="white").grid(row=1, column=0, padx=2, pady=2)
        ttk.Combobox(student_frame, textvariable=self.var_gender, font=("times new roman", 10), state="readonly", width=15,
                      values=("Male", "Female", "Other")).grid(row=1, column=1, padx=2, pady=2)
        
        tk.Label(student_frame, text="Phone:", font=("times new roman", 10), bg="white").grid(row=1, column=2, padx=2, pady=2)
        ttk.Entry(student_frame, textvariable=self.var_phone, font=("times new roman", 10), width=10).grid(row=1, column=3, padx=2, pady=2)
        
        # DOB & Email (row 2)
        tk.Label(student_frame, text="DOB:", font=("times new roman", 10), bg="white").grid(row=2, column=0, padx=2, pady=2)
        ttk.Entry(student_frame, textvariable=self.var_dob, font=("times new roman", 10), width=15).grid(row=2, column=1, padx=2, pady=2)
        
        tk.Label(student_frame, text="Email:", font=("times new roman", 10), bg="white").grid(row=2, column=2, padx=2, pady=2)
        ttk.Entry(student_frame, textvariable=self.var_email, font=("times new roman", 10), width=10).grid(row=2, column=3, padx=2, pady=2)
        
        # Name (row 3)
        tk.Label(student_frame, text="Name:", font=("times new roman", 10), bg="white").grid(row=3, column=0, padx=2, pady=2)
        ttk.Entry(student_frame, textvariable=self.var_name, font=("times new roman", 10), width=15).grid(row=3, column=1, padx=2, pady=2)
        
        # Address (row 4)
        tk.Label(student_frame, text="Address:", font=("times new roman", 10), bg="white").grid(row=4, column=0, padx=2, pady=2)
        ttk.Entry(student_frame, textvariable=self.var_address, font=("times new roman", 10), width=15).grid(row=4, column=1, padx=2, pady=2)
        
        # Photo Sample
        ttk.Radiobutton(student_frame, variable=self.var_radio1, text="Photo", value="Yes").grid(row=4, column=2, padx=2, pady=2)
        ttk.Radiobutton(student_frame, variable=self.var_radio1, text="No Photo", value="No").grid(row=4, column=3, padx=2, pady=2)
        
        # Buttons Frame
        btn_frame = tk.Frame(student_frame, bd=2, relief=tk.RIDGE, bg="white")
        btn_frame.place(x=5, y=150, width=320, height=150)
        
        # Buttons (2x2 grid)
        btn_save = tk.Button(btn_frame, text="Save", command=self.add_data, width=15, font=("times new roman", 10), bg="#004d99", fg="white")
        btn_save.grid(row=0, column=0, padx=5, pady=5)
        
        btn_update = tk.Button(btn_frame, text="Update", command=self.update_data, width=15, font=("times new roman", 10), bg="#004d99", fg="white")
        btn_update.grid(row=0, column=1, padx=5, pady=5)
        
        btn_delete = tk.Button(btn_frame, text="Delete", command=self.delete_data, width=15, font=("times new roman", 10), bg="#004d99", fg="white")
        btn_delete.grid(row=1, column=0, padx=5, pady=5)
        
        btn_reset = tk.Button(btn_frame, text="Reset", command=self.reset_data, width=15, font=("times new roman", 10), bg="#004d99", fg="white")
        btn_reset.grid(row=1, column=1, padx=5, pady=5)
        
        btn_photo = tk.Button(btn_frame, text="Take Photo", command=self.take_photo, width=15, font=("times new roman", 10), bg="#004d99", fg="white")
        btn_photo.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Right Frame (Table & Search)
        right_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE, text="Student Records", font=("times new roman", 10, "bold"))
        right_frame.place(x=360, y=5, width=520, height=545)
        
        # Search Frame
        search_frame = tk.LabelFrame(right_frame, bd=2, bg="white", relief=tk.RIDGE, text="Search", font=("times new roman", 10, "bold"))
        search_frame.place(x=5, y=5, width=505, height=60)
        
        # Search Components
        tk.Label(search_frame, text="Search By:", font=("times new roman", 10), bg="white").grid(row=0, column=0, padx=2, pady=2)
        
        combo_search = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("times new roman", 10), state="readonly", width=10)
        combo_search["values"] = ("ID", "Phone", "Email")
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=2, pady=2)
        
        txt_search = ttk.Entry(search_frame, textvariable=self.var_search_txt, font=("times new roman", 10), width=15)
        txt_search.grid(row=0, column=2, padx=2, pady=2)
        
        btn_search = tk.Button(search_frame, text="Search", command=self.search_data, width=8, font=("times new roman", 10), bg="#004d99", fg="white")
        btn_search.grid(row=0, column=3, padx=2, pady=2)
        
        btn_show_all = tk.Button(search_frame, text="Show All", command=self.fetch_data, width=8, font=("times new roman", 10), bg="#004d99", fg="white")
        btn_show_all.grid(row=0, column=4, padx=2, pady=2)
        
        # Table Frame
        table_frame = tk.Frame(right_frame, bd=2, bg="white", relief=tk.RIDGE)
        table_frame.place(x=5, y=70, width=505, height=460)
        
        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Student Table with smaller columns
        self.student_table = ttk.Treeview(table_frame, columns=("id", "dep", "course", "div", "phone", "email"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        
        # Configure columns
        self.student_table.heading("id", text="ID")
        self.student_table.heading("dep", text="Dept")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("div", text="Div")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("email", text="Email")
        
        self.student_table["show"] = "headings"
        
        # Set column widths
        self.student_table.column("id", width=50)
        self.student_table.column("dep", width=50)
        self.student_table.column("course", width=60)
        self.student_table.column("div", width=40)
        self.student_table.column("phone", width=80)
        self.student_table.column("email", width=100)
        
        self.student_table.pack(fill=tk.BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        
        # Migrate database and create table
        migrate_database()
        self.create_db()
        self.fetch_data()
    
    # DATABASE FUNCTIONS
    
    def create_db(self):
        conn = sqlite3.connect("student_small.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                    dep TEXT, course TEXT, year TEXT, semester TEXT, 
                    id TEXT PRIMARY KEY, division TEXT, gender TEXT, 
                    phone TEXT, dob TEXT, email TEXT, address TEXT, 
                    name TEXT, photo TEXT DEFAULT 'No')''')
        conn.commit()
        conn.close()
    
    def add_data(self):
        if self.var_dep.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect("student_small.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM student WHERE id=?", (self.var_std_id.get(),))
                row = cursor.fetchone()
                
                if row:
                    messagebox.showerror("Error", f"ID {self.var_std_id.get()} already exists", parent=self.root)
                else:
                    # Use photo value from radio button or default to 'No'
                    photo_status = self.var_radio1.get() if self.var_radio1.get() else 'No'
                    
                    cursor.execute("INSERT INTO student VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_dep.get(), 
                        self.var_course.get(), 
                        self.var_year.get(), 
                        self.var_semester.get(), 
                        self.var_std_id.get(), 
                        self.var_div.get(),
                        self.var_gender.get(), 
                        self.var_phone.get(), 
                        self.var_dob.get(),
                        self.var_email.get(), 
                        self.var_address.get(), 
                        self.var_name.get(),
                        photo_status
                    ))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Record added successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)
    
    def fetch_data(self):
        conn = sqlite3.connect("student_small.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, dep, course, division, phone, email FROM student")
        data = cursor.fetchall()
        
        self.student_table.delete(*self.student_table.get_children())
        for i in data:
            self.student_table.insert("", tk.END, values=i)
        conn.close()
    
    def get_cursor(self, event=""):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        data = content["values"]
        
        if data:
            # Get full record based on ID
            conn = sqlite3.connect("student_small.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student WHERE id=?", (data[0],))
            full_data = cursor.fetchone()
            conn.close()
            
            if full_data:
                self.var_dep.set(full_data[0])
                self.var_course.set(full_data[1])
                self.var_year.set(full_data[2])
                self.var_semester.set(full_data[3])
                self.var_std_id.set(full_data[4])
                self.var_div.set(full_data[5])
                self.var_gender.set(full_data[6])
                self.var_phone.set(full_data[7])
                self.var_dob.set(full_data[8])
                self.var_email.set(full_data[9])
                self.var_address.set(full_data[10])
                self.var_name.set(full_data[11])
                # Set radio button for photo if needed
                self.var_radio1.set(full_data[12] if full_data[12] else 'No')
    
    def update_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "ID is required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect("student_small.db")
                cursor = conn.cursor()
                # Use photo value from radio button or default to 'No'
                photo_status = self.var_radio1.get() if self.var_radio1.get() else 'No'
                
                cursor.execute("""UPDATE student SET 
                    dep=?, course=?, year=?, semester=?, 
                    division=?, gender=?, phone=?, dob=?, 
                    email=?, address=?, name=?, photo=? 
                    WHERE id=?""", (
                    self.var_dep.get(), 
                    self.var_course.get(), 
                    self.var_year.get(), 
                    self.var_semester.get(), 
                    self.var_div.get(), 
                    self.var_gender.get(),
                    self.var_phone.get(), 
                    self.var_dob.get(), 
                    self.var_email.get(),
                    self.var_address.get(), 
                    self.var_name.get(), 
                    photo_status,
                    self.var_std_id.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Record updated successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)
    
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "ID is required", parent=self.root)
        else:
            try:
                if messagebox.askyesno("Delete", "Delete this record?", parent=self.root):
                    conn = sqlite3.connect("student_small.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM student WHERE id=?", (self.var_std_id.get(),))
                    conn.commit()
                    conn.close()
                    self.fetch_data()
                    self.reset_data()
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)
    
    def reset_data(self):
        self.var_dep.set("")
        self.var_course.set("")
        self.var_year.set("")
        self.var_semester.set("")
        self.var_std_id.set("")
        self.var_div.set("")
        self.var_gender.set("")
        self.var_phone.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_address.set("")
        self.var_name.set("")
        self.var_radio1.set("")
    
    def search_data(self):
        if self.var_search_by.get() == "" or self.var_search_txt.get() == "":
            messagebox.showerror("Error", "Select search option and enter value", parent=self.root)
        else:
            try:
                conn = sqlite3.connect("student_small.db")
                cursor = conn.cursor()
                
                if self.var_search_by.get() == "ID":
                    cursor.execute("SELECT id, dep, course, division, phone, email FROM student WHERE id LIKE ?", 
                                  ('%' + self.var_search_txt.get() + '%',))
                elif self.var_search_by.get() == "Phone":
                    cursor.execute("SELECT id, dep, course, division, phone, email FROM student WHERE phone LIKE ?", 
                                  ('%' + self.var_search_txt.get()+ '%',))
                elif self.var_search_by.get() == "Email":
                    cursor.execute("SELECT id, dep, course, division, phone, email FROM student WHERE email LIKE ?", 
                                  ('%' + self.var_search_txt.get() + '%',))
                
                data = cursor.fetchall()
                
                if len(data) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in data:
                        self.student_table.insert("", tk.END, values=i)
                else:
                    messagebox.showinfo("Info", "No matching records found", parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)
    
    def take_photo(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID required", parent=self.root)
        else:
            try:
                # Set the desired path for saving photos
                path = r"student_photos"
                os.makedirs(path, exist_ok=True)  # Create directory if it doesn't exist
                
                # Open camera in a separate window
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    messagebox.showerror("Error", "Camera not available", parent=self.root)
                    return
                    
                # Create popup window for photo
                photo_window = tk.Toplevel(self.root)
                photo_window.title("Take Photo")
                photo_window.geometry("400x400")
                
                # Label to display camera feed
                img_label = tk.Label(photo_window)
                img_label.pack(pady=10)
                
                # Instructions
                tk.Label(photo_window, text="Press 'c' to capture (3 photos will be taken)", font=("times new roman", 10)).pack(pady=5)
                photo_window.focus_force()
                
                # Counter for photos
                photo_count = [0]  # Using list for nonlocal access
                max_photos = 3
                frame = None  # Initialize frame variable
                
                def update_feed():
                    nonlocal frame  # Use the frame variable from the outer scope
                    ret, frame = cap.read()
                    if ret:
                        frame = cv2.resize(frame, (320, 240))
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(img)
                        img = ImageTk.PhotoImage(img)
                        img_label.configure(image=img)
                        img_label.image = img
                        photo_window.after(10, update_feed)
                    else:
                        cap.release()
                        photo_window.destroy()
                
                def capture_photo(event):
                    nonlocal frame  # Use the frame variable from the outer scope
                    if photo_count[0] < max_photos:
                        # Save image
                        photo_count[0] += 1
                        filename = os.path.join(path, f"{self.var_std_id.get()}_{photo_count[0]}.jpg")
                        cv2.imwrite(filename, frame)
                        messagebox.showinfo("Success", f"Photo {photo_count[0]} captured", parent=photo_window)
                        
                        # Update DB
                        conn = sqlite3.connect("student_small.db")
                        cursor = conn.cursor()
                        cursor.execute("UPDATE student SET photo=? WHERE id=?", ("Yes", self.var_std_id.get()))
                        conn.commit()
                        conn.close()
                        
                        if photo_count[0] >= max_photos:
                            cap.release()
                            photo_window.destroy()
                            self.fetch_data()
                            return
            
                # Bind the 'c' key to the capture_photo function
                photo_window.bind('<c>', capture_photo)
                
                update_feed()
                
                def on_closing():
                    cap.release()
                    photo_window.destroy()
                
                photo_window.protocol("WM_DELETE_WINDOW", on_closing)
                
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    obj = StudentManagementSystem(root)
    root.mainloop()