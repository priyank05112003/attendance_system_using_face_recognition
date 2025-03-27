import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox, Label, Button
import sqlite3
import warnings
import time
import logging

class Face_Recognition:
    def __init__(self, root):
        self.root = root  
        self.root.geometry("1200x600+100+50")
        self.root.title("Face Recognition System")
        
        # Configure logging
        logging.basicConfig(filename='face_recognition.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Title Label
        title_lbl = Label(root, text="FACE RECOGNITION SYSTEM", 
                         font=("times new roman", 35, "bold"), 
                         bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1200, height=45)
        
        # Recognition Info Label
        self.recognized_info_lbl = Label(root, text="", 
                                       font=("times new roman", 20, "bold"), 
                                       bg="white", fg="blue")
        self.recognized_info_lbl.place(x=20, y=50, width=400, height=40)
        
        # Confidence Label
        self.confidence_lbl = Label(root, text="Confidence: --%", 
                                  font=("times new roman", 16), 
                                  bg="white", fg="black")
        self.confidence_lbl.place(x=450, y=50, width=300, height=40)
        
        # Status Label
        self.status_lbl = Label(root, text="Status: Ready", 
                              font=("times new roman", 14), 
                              bg="white", fg="black")
        self.status_lbl.place(x=800, y=50, width=300, height=40)
        
        # Load Images
        self.load_images()
        
        # Recognition Button
        Button(root, text="Start Face Recognition", cursor="hand2", 
               font=("times new roman", 18), bg="navy blue", fg="pink", 
               command=self.face_recog).place(x=850, y=480, width=200, height=40)
    
    def load_images(self):
        """Load and display background images"""
        try:
            # Top Image
            img_top = Image.open(r"C:\Users\KIIT\OneDrive\Documents\imagewhd\1234ewmdkeolc.jpg")
            img_top = img_top.resize((600, 400), Image.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            Label(self.root, image=self.photoimg_top).place(x=0, y=100, width=600, height=400)
            
            # Bottom Image
            img_bottom = Image.open(r"C:\Users\KIIT\OneDrive\Documents\imagewhd\wtwwy.jpg")
            img_bottom = img_bottom.resize((600, 400), Image.LANCZOS)
            self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
            Label(self.root, image=self.photoimg_bottom).place(x=600, y=100, width=600, height=400)
        except Exception as e:
            logging.error(f"Error loading images: {e}")
            messagebox.showerror("Image Load Error", str(e))

    def preprocess_face(self, face_img, target_size=(200, 200)):
        """Enhanced face preprocessing pipeline"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            
            # Apply histogram equalization
            gray = cv2.equalizeHist(gray)
            
            # Apply Gaussian blur
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Normalize pixel values
            gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
            
            # Resize to consistent size
            gray = cv2.resize(gray, target_size)
            
            return gray
        except Exception as e:
            logging.error(f"Face preprocessing error: {e}")
            return None

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, recognizer):
        """Enhanced face detection and recognition with robust error handling"""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = classifier.detectMultiScale(gray, scaleFactor, minNeighbors)

            for (x, y, w, h) in faces:
                face_roi = img[y:y+h, x:x+w]
                
                # Preprocess face
                processed_face = self.preprocess_face(face_roi)
                
                if processed_face is None:
                    self.show_unknown_face(img, x, y, w, h, "Preprocessing Failed")
                    continue
                
                try:
                    id, confidence = recognizer.predict(processed_face)
                    
                    # Advanced confidence normalization
                    confidence_percent = max(0, min(100, int(100 * (1 - confidence / 300))))
                    
                    self.confidence_lbl.config(text=f"Confidence: {confidence_percent}%")
                    
                    # More flexible confidence threshold
                    if confidence_percent > 40:  # Adjusted threshold
                        # Get student info from database
                        conn = sqlite3.connect("student_small.db")
                        cursor = conn.cursor()
                        cursor.execute("SELECT name, dep, id FROM student WHERE id=?", (id,))
                        result = cursor.fetchone()
                        conn.close()

                        if result:
                            name, dep, student_id = result
                            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(img, f"ID: {student_id}", (x, y-50), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                            cv2.putText(img, f"Name: {name}", (x, y-20), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                            
                            self.recognized_info_lbl.config(text=f"Recognized: {name} (ID: {student_id})")
                            self.status_lbl.config(text="Status: Recognized")
                            
                            # Log successful recognition
                            logging.info(f"Recognized: {name} (ID: {student_id}) with {confidence_percent}% confidence")
                        else:
                            self.show_unknown_face(img, x, y, w, h, "No Database Record")
                    else:
                        self.show_unknown_face(img, x, y, w, h, f"Low Confidence ({confidence_percent}%)")
                
                except Exception as e:
                    logging.error(f"Recognition error: {e}")
                    self.show_unknown_face(img, x, y, w, h, "Recognition Error")
        
        except Exception as global_e:
            logging.error(f"Global detection error: {global_e}")
            messagebox.showerror("Detection Error", str(global_e))

    def show_unknown_face(self, img, x, y, w, h, reason):
        """Comprehensive unknown face handling"""
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(img, f"Unknown ({reason})", (x, y-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        self.recognized_info_lbl.config(text=f"Unknown Face ({reason})")
        self.status_lbl.config(text="Status: Unknown Face")
        
        # Log unknown faces
        logging.warning(f"Unknown face detected: {reason}")

    def load_recognizer(self):
        """Robust recognizer loading with multiple fallback mechanisms"""
        recognizer_paths = [
            "trained_model.yml",  # Primary model
            "backup_model.yml",   # Optional backup model
        ]
        
        for model_path in recognizer_paths:
            try:
                if not os.path.exists(model_path):
                    logging.warning(f"Model {model_path} not found")
                    continue
                
                # Try different recognizer types
                recognizer_types = [
                    cv2.face.LBPHFaceRecognizer_create,
                    cv2.face.FisherFaceRecognizer_create,
                    cv2.face.EigenFaceRecognizer_create
                ]
                
                for recognizer_type in recognizer_types:
                    try:
                        recognizer = recognizer_type()
                        recognizer.read(model_path)
                        logging.info(f"Successfully loaded model: {model_path}")
                        return recognizer
                    except Exception as type_e:
                        logging.warning(f"Failed with {recognizer_type.__name__}: {type_e}")
            
            except Exception as e:
                logging.error(f"Error loading model {model_path}: {e}")
        
        raise FileNotFoundError("No valid face recognition model found")

    def face_recog(self):
        """Main face recognition function with comprehensive error handling"""
        try:
            self.status_lbl.config(text="Status: Initializing...")
            self.root.update()
            
            # Load recognizer with error handling
            try:
                recognizer = self.load_recognizer()
            except FileNotFoundError:
                messagebox.showerror("Model Error", "No trained face recognition model found. Please train the model first.")
                return
            
            # Load face detector
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Initialize webcam with multiple checks
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                messagebox.showerror("Camera Error", "Could not open webcam. Please check your camera connection.")
                return
            
            cap.set(3, 640)  # Width
            cap.set(4, 480)  # Height
            
            # Reset UI
            self.recognized_info_lbl.config(text="")
            self.confidence_lbl.config(text="Confidence: --%")
            self.status_lbl.config(text="Status: Running...")
            
            # Webcam warmup
            for _ in range(10):
                cap.read()
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    self.status_lbl.config(text="Status: Camera Error")
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Face detection with adjusted parameters
                self.draw_boundary(frame, face_cascade, 1.2, 4, (0, 255, 0), recognizer)
                
                cv2.imshow("Face Recognition - Press Q to quit", frame)
                
                # Exit conditions
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # Q or ESC key
                    self.status_lbl.config(text="Status: Stopped by user")
                    break
            
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            logging.error(f"Face recognition error: {e}")
            messagebox.showerror("Recognition Error", f"An unexpected error occurred: {str(e)}")
            self.status_lbl.config(text=f"Status: Error - {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    obj = Face_Recognition(root)
    root.mainloop()