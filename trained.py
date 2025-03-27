import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox
import warnings
import re

class Trained:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600+100+50")
        self.root.title("Face Recognition System")
        
        # Title Label
        title_lbl = tk.Label(root, text="TRAIN DATA SET", 
                           font=("times new roman", 30, "bold"), fg="blue")
        title_lbl.place(x=0, y=0, width=900, height=45)
        
        # Load Images
        self.load_images()
        
        # Train Data Button
        tk.Button(root, text="Train Data", cursor="hand2",
                 font=("times new roman", 18, "bold"), fg="red",
                 command=self.train_classifier).place(x=300, y=500, width=300, height=50)

    def load_images(self):
        """Load and display background images"""
        try:
            # Top Image
            img_top = Image.open(r"C:\Users\KIIT\OneDrive\Documents\imagewhd\1f37a9a2-af5c-4511-b8de-68fdd4c93a93.webp")
            img_top = img_top.resize((900, int(900 * img_top.height/img_top.width)), Image.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            tk.Label(self.root, image=self.photoimg_top).place(x=0, y=230)
            
            # Bottom Image
            img_bottom = Image.open(r"C:\Users\KIIT\OneDrive\Documents\imagewhd\WhatsApp Image 2025-02-06 at 11.58.14_8fb7bf65.jpg")
            img_bottom = img_bottom.resize((900, int(900 * img_bottom.height/img_bottom.width)), Image.LANCZOS)
            self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
            tk.Label(self.root, image=self.photoimg_bottom).place(x=0, y=400)
        except Exception as e:
            warnings.warn(f"Image loading error: {e}")

    def preprocess_face(self, face_img, target_size=(200, 200)):
        """Preprocess and resize face images consistently"""
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        return cv2.resize(gray, target_size)

    def extract_id_from_filename(self, filename):
        """
        Extract ID from filename with multiple formats:
        - "user1 (104).jpg" -> returns 104
        - "user1.jpg" -> returns 1
        - "104_user1.jpg" -> returns 104
        """
        try:
            # Try to find number in parentheses first
            match = re.search(r'\((\d+)\)', filename)
            if match:
                return int(match.group(1))
            
            # Try to find number after "user"
            match = re.search(r'user(\d+)', filename, re.IGNORECASE)
            if match:
                return int(match.group(1))
            
            # Try to find number at start of filename
            match = re.search(r'^(\d+)', filename)
            if match:
                return int(match.group(1))
                
            raise ValueError("No ID found in filename")
        except Exception as e:
            warnings.warn(f"Cannot extract ID from {filename}: {str(e)}")
            return None

    def train_classifier(self):
        """Train face recognition model with proper resizing"""
        data_dir = r"C:\Users\KIIT\OneDrive\Documents\AD_Lab-current\open_ended_project\images"
        
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", f"Directory not found: {data_dir}")
            return
        
        # Initialize face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        faces = []
        ids = []
        target_size = (200, 200)  # Fixed size for all images
        processed_count = 0
        
        for file in os.listdir(data_dir):
            if not file.lower().endswith(('.jpg', '.png', '.jpeg')):
                continue
                
            image_path = os.path.join(data_dir, file)
            try:
                img = cv2.imread(image_path)
                if img is None:
                    warnings.warn(f"Could not read image: {file}")
                    continue
                    
                # Detect and preprocess face
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                detected_faces = face_cascade.detectMultiScale(gray, 1.1, 5)
                
                if len(detected_faces) == 0:
                    warnings.warn(f"No face detected in: {file}")
                    continue
                    
                (x, y, w, h) = detected_faces[0]
                face_roi = img[y:y+h, x:x+w]
                processed_face = self.preprocess_face(face_roi, target_size)
                
                # Extract ID from filename
                id = self.extract_id_from_filename(file)
                if id is None:
                    continue
                    
                faces.append(processed_face)
                ids.append(id)
                processed_count += 1
                
                cv2.imshow("Training", processed_face)
                if cv2.waitKey(1) == 13:  # Exit on Enter
                    break
                
            except Exception as e:
                warnings.warn(f"Error processing {file}: {e}")
    
        if processed_count < 2:  # Fisherfaces requires at least 2 samples
            messagebox.showerror("Error", f"Need at least 2 face samples to train (found {processed_count})")
            cv2.destroyAllWindows()
            return
        
        # Try Fisherfaces first, fallback to LBPH if fails
        try:
            recognizer = cv2.face.FisherFaceRecognizer_create()
            recognizer.train(faces, np.array(ids))
            recognizer.save("trained_model.yml")
            messagebox.showinfo("Success", 
                              f"Fisherfaces model trained with {processed_count} samples\nSaved as 'trained_model.yml'")
        except Exception as e:
            warnings.warn(f"Fisherfaces failed: {e}. Trying LBPH...")
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.train(faces, np.array(ids))
                recognizer.save("trained_model.yml")
                messagebox.showinfo("Success", 
                                  f"LBPH model trained with {processed_count} samples\n(Fisherfaces failed)\nSaved as 'trained_model.yml'")
            except Exception as e:
                messagebox.showerror("Error", f"Training failed: {str(e)}")
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    obj = Trained(root)
    root.mainloop()