import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import os
import pickle
from pymongo import MongoClient
import face_recognition

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["attendance_system"]
students_collection = db["students"]
attendance_collection = db["attendance_records"]

# Directory for storing student images
students_dir = "known_faces"
os.makedirs(students_dir, exist_ok=True)

# Path to model file
model_file = "A_model.pkl"
if not os.path.exists(model_file):
    # Create an empty model file if it doesn't exist
    with open(model_file, "wb") as file:
        pickle.dump({"encodings": [], "names": []}, file)

# Functions
def capture_photo(name):
    """Open webcam, capture a photo, and save it."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Unable to access the webcam!")
        return False

    messagebox.showinfo("Info", "Press 'SPACE' to capture the photo, then 'ESC' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image!")
            cap.release()
            return False

        cv2.imshow("Capture Photo", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # SPACE key to capture
            photo_path = os.path.join(students_dir, f"{name}.jpg")
            cv2.imwrite(photo_path, frame)
            cap.release()
            cv2.destroyAllWindows()
            return photo_path
        elif key == 27:  # ESC key to cancel
            cap.release()
            cv2.destroyAllWindows()
            return None

def add_student():
    """Add a new student by capturing their photo and updating the encodings."""
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter the name!")
        return

    # Check if the student already exists
    if students_collection.find_one({"name": name}):
        messagebox.showerror("Error", "Student with this name already exists!")
        return

    # Capture the student's photo
    photo_path = capture_photo(name)
    if not photo_path:
        return

    # Generate face encoding
    image = face_recognition.load_image_file(photo_path)
    encoding = face_recognition.face_encodings(image)
    if not encoding:
        messagebox.showerror("Error", "No face detected in the captured photo!")
        os.remove(photo_path)  # Remove the photo if no face is detected
        return

    # Update the model file
    with open(model_file, "rb") as file:
        data = pickle.load(file)

    data["encodings"].append(encoding[0])
    data["names"].append(name)

    with open(model_file, "wb") as file:
        pickle.dump(data, file)

    # Add the student to the database
    students_collection.insert_one({"name": name})

    messagebox.showinfo("Success", f"Student {name} added successfully!")

    # Clear the input fields
    name_entry.delete(0, tk.END)

def view_attendance():
    """View attendance records in a new window."""
    # Retrieve all attendance records
    attendance_data = list(attendance_collection.find({}).sort([("date", 1), ("timestamp", 1)]))

    # Create a Tkinter window
    attendance_window = tk.Toplevel()
    attendance_window.title("Attendance Records")
    attendance_window.geometry("800x400")

    # Set up the table
    columns = ["Name", "Date", "Timestamp"]
    tree = ttk.Treeview(attendance_window, columns=columns, show="headings", height=20)

    # Define column headers
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")

    # Insert data into the table
    for record in attendance_data:
        tree.insert("", "end", values=(record["name"], record["date"], record["timestamp"]))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(attendance_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Pack the table
    tree.pack(fill="both", expand=True)

# GUI Setup
root = tk.Tk()
root.title("Attendance Management System")

# Frames
top_frame = tk.Frame(root, padx=10, pady=10)
top_frame.pack(fill=tk.X)

# Add Student Section
tk.Label(top_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(top_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

add_button = tk.Button(top_frame, text="Add Student", command=add_student)
add_button.grid(row=0, column=2, padx=5, pady=5)

view_button = tk.Button(top_frame, text="View Attendance", command=view_attendance)
view_button.grid(row=0, column=3, padx=5, pady=5)

# Start the application
root.geometry("800x600")
root.mainloop()
