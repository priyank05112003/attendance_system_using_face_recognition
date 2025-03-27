import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys
from datetime import datetime
import webbrowser
from student import StudentManagementSystem  # Import the StudentManagementSystem class
from trained import Trained  # Import the Trained class
from face_recognition import Face_Recognition  # Import the Face_Recognition class
from attendance import  Attendance
class FaceRecognitionSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Recognition Attendance System")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1200, screen_width)
        window_height = min(800, screen_height)
        
        # Center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Color scheme (modern and professional)
        self.colors = {
            'primary': '#1976D2',      # Primary blue
            'primary_dark': '#0D47A1', # Dark blue
            'accent': '#00C853',       # Green accent
            'background': '#F5F5F5',   # Light gray background
            'card': '#FFFFFF',         # White card background
            'text_light': '#FFFFFF',   # White text
            'text_dark': '#212121',    # Dark text
            'text_muted': '#757575'    # Muted text
        }
        
        # Set default font
        self.default_font = ("Helvetica", 10)
        self.title_font = ("Helvetica", 24, "bold")
        self.subtitle_font = ("Helvetica", 14)
        self.button_font = ("Helvetica", 12, "bold")
        
        # Configure the main frame with a modern look
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.main_frame.pack(fill="both", expand=True)
        
        # Create header
        self.create_header()
        
        # Create content area
        self.create_content()
        
        # Create status bar
        self.create_status_bar()
    
    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.main_frame, bg=self.colors['primary'], height=100)
        header_frame.pack(fill="x")
        
        # App title
        title = tk.Label(
            header_frame,
            text="FACE RECOGNITION ATTENDANCE SYSTEM",
            font=self.title_font,
            bg=self.colors['primary'],
            fg=self.colors['text_light'],
            pady=25
        )
        title.pack()
    
    def create_content(self):
        # Content frame with some padding
        content_frame = tk.Frame(self.main_frame, bg=self.colors['background'], padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Welcome message
        welcome_frame = tk.Frame(content_frame, bg=self.colors['card'], padx=20, pady=15)
        welcome_frame.pack(fill="x", pady=10)
        
        welcome_text = f"Welcome to the Face Recognition Attendance System\nCurrent Time: {datetime.now().strftime('%I:%M %p')}"
        welcome = tk.Label(
            welcome_frame,
            text=welcome_text,
            font=self.subtitle_font,
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        )
        welcome.pack(anchor="w")
        
        # Create feature buttons in a grid
        buttons_frame = tk.Frame(content_frame, bg=self.colors['background'])
        buttons_frame.pack(fill="both", expand=True, pady=10)
        
        # Define button specs
        self.buttons = [
            {"text": "Student Details", "icon": "👤", "row": 0, "column": 0, "command": self.student_details},
            {"text": "Face Detector", "icon": "🔍", "row": 0, "column": 1, "command": self.face_data},  # Updated command
            {"text": "Attendance", "icon": "📋", "row": 0, "column": 2, "command": self.attendance_data},
            {"text": "Help Desk", "icon": "❓", "row": 0, "column": 3, "command": lambda: self.button_click("Help Desk")},
            {"text": "Train Data", "icon": "🧠", "row": 1, "column": 0, "command": self.train_data},
            {"text": "Photos", "icon": "📸", "row": 1, "column": 1, "command": self.show_photos},  # Updated command
            {"text": "Developer", "icon": "💻", "row": 1, "column": 2, "command": lambda: self.button_click("Developer")},
            {"text": "Exit", "icon": "🚪", "row": 1, "column": 3, "command": lambda: self.button_click("Exit")}
        ]
        
        # Create each button
        for button in self.buttons:
            self.create_feature_button(buttons_frame, **button)
    
    def create_feature_button(self, parent, text, icon, row, column, command):
        # Create button frame with card-like appearance
        button_frame = tk.Frame(
            parent,
            bg=self.colors['card'],
            padx=20,
            pady=20,
            highlightbackground=self.colors['primary'],
            highlightthickness=1,
            relief="flat"
        )
        button_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Configure hovering effect
        button_frame.bind("<Enter>", lambda event, f=button_frame: self.on_hover(f, True))
        button_frame.bind("<Leave>", lambda event, f=button_frame: self.on_hover(f, False))
        button_frame.bind("<Button-1>", lambda event, cmd=command: cmd())
        
        # Add icon (emoji as a simple non-image alternative)
        icon_label = tk.Label(
            button_frame,
            text=icon,
            font=("Helvetica", 40),
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        icon_label.pack(pady=(10, 15))
        
        # Add button text
        text_label = tk.Label(
            button_frame,
            text=text,
            font=self.button_font,
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        )
        text_label.pack()
        
        # Make labels clickable too
        icon_label.bind("<Button-1>", lambda event, cmd=command: cmd())
        text_label.bind("<Button-1>", lambda event, cmd=command: cmd())
        
        # Make the grid cells expandable
        parent.grid_columnconfigure(column, weight=1)
        parent.grid_rowconfigure(row, weight=1)
    
    def on_hover(self, frame, is_hovering):
        if is_hovering:
            frame.config(bg="#E3F2FD", highlightbackground=self.colors['accent'])
            for widget in frame.winfo_children():
                widget.config(bg="#E3F2FD")
        else:
            frame.config(bg=self.colors['card'], highlightbackground=self.colors['primary'])
            for widget in frame.winfo_children():
                widget.config(bg=self.colors['card'])
    
    def create_status_bar(self):
        # Status bar
        status_frame = tk.Frame(self.main_frame, bg=self.colors['primary_dark'], height=30)
        status_frame.pack(fill="x", side="bottom")
        
        # Status message
        status = tk.Label(
            status_frame,
            text="Ready | System initialized successfully",
            font=self.default_font,
            bg=self.colors['primary_dark'],
            fg=self.colors['text_light'],
            anchor="w",
            padx=10,
            pady=5
        )
        status.pack(side="left")
        
        # Clock
        self.clock_label = tk.Label(
            status_frame,
            text="",
            font=self.default_font,
            bg=self.colors['primary_dark'],
            fg=self.colors['text_light'],
            padx=10,
            pady=5
        )
        self.clock_label.pack(side="right")
        self.update_clock()
    
    def update_clock(self):
        time_string = datetime.now().strftime("%I:%M:%S %p")
        self.clock_label.config(text=time_string)
        self.root.after(1000, self.update_clock)
    
    def student_details(self):
        self.new_window = tk.Toplevel(self.root)
        self.app = StudentManagementSystem(self.new_window)
    
    def train_data(self):
        self.new_window = tk.Toplevel(self.root)  # Create a new window
        self.app = Trained(self.new_window)  # Open the Trained window

    def face_data(self):
        self.new_window = tk.Toplevel(self.root)  # Create a new window
        self.app = Face_Recognition(self.new_window)  # Open the Face_Recognition window

    def attendance_data(self):
        self.new_window=tk.Toplevel(self.root)
        self.app= Attendance(self.new_window)
    def show_photos(self):
        # Path to the directory where images are saved
        image_directory = r"C:\Users\KIIT\OneDrive\Documents\AD_Lab-current\open_ended_project\picture_click"
        
        # Get the list of image files in the directory
        image_files = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            messagebox.showinfo("No Images", "No images found in the specified directory.")
            return
        
        # Create a new window to display the image
        self.photo_window = tk.Toplevel(self.root)
        self.photo_window.title("Photos")
        
        # Load the first image
        image_path = os.path.join(image_directory, image_files[0])
        img = Image.open(image_path)
        img = img.resize((600, 400), Image.LANCZOS)  # Resize to fit the window
        self.photo_img = ImageTk.PhotoImage(img)
        
        # Display the image
        img_label = tk.Label(self.photo_window, image=self.photo_img)
        img_label.pack(padx=10, pady=10)
        
        # Close button
        close_button = tk.Button(self.photo_window, text="Close", command=self.photo_window.destroy)
        close_button.pack(pady=10)

    def button_click(self, text):
        if text == "Exit":
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                self.root.quit()
        elif text == "Help Desk":
            webbrowser.open("mailto:priyankshekhar0511@gmail.com?subject=Help Desk Inquiry&body=Hello,")
        else:
            messagebox.showinfo("Feature", f"The '{text}' feature is coming soon!")
    
    def run(self):
        # Configure grid weights to make the layout responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Run the application
        self.root.mainloop()

if __name__ == "__main__":
    app = FaceRecognitionSystem()
    app.run()