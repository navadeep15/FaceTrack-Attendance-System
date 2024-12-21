# Attendance Management System

This project is an automated attendance management system that uses face recognition to mark the attendance of students. The system consists of three main components:

1. **Training Module**
2. **Attendance Capture Module**
3. **Student Management and Attendance Viewing Module**

## Features

- Face recognition-based attendance marking.
- Student photo and encoding management.
- Attendance record storage using MongoDB.
- GUI for adding students and viewing attendance.
- Real-time webcam-based face detection.

---

## Prerequisites

Before using this project, ensure you have the following installed:

1. **Python** (>=3.6)
2. Required Python libraries:
   - `face_recognition`
   - `opencv-python`
   - `numpy`
   - `pymongo`
   - `tkinter`
   - `pickle`

   Install Python libraries using:
```bash
pip install face_recognition opencv-python numpy pymongo tkinter pickle
```
3. **MongoDB**

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/navadeep15/FaceTrack-Attendance-System.git
   cd FaceTrack-Attendance-System
   ```

2. **Prepare student directory**
   - Create a folder named `known_faces` in the project directory to store student images.

3. **Run MongoDB**
   - Start your MongoDB server locally or use a connection string for a remote database.

4. **Train the Model**
   - Use the `Training.py` script to process student images and generate encodings.
   - Ensure the `known_faces` folder contains images in `.jpg` or `.png` format before running the script.
   - Command:
     ```bash
     python Training.py
     ```

5. **Start the Attendance System**
   - Use the `Take_attendance.py` script to open the webcam and mark attendance.
   - Command:
     ```bash
     python Take_attendance.py
     ```

6. **Add New Students and View Attendance**
   - Run the `Add_new_face.py` script for GUI-based student management.
   - Command:
     ```bash
     python Add_new_face.py
     ```

---

## File Descriptions

### 1. `Training.py`
- Processes all images in the `known_faces` folder.
- Generates face encodings and saves them to `A_model.pkl`.
- **Output:** `A_model.pkl` file containing student encodings and names.

### 2. `Take_attendance.py`
- Uses webcam to detect faces in real-time.
- Compares detected faces with known encodings to mark attendance.
- Stores attendance records in MongoDB with fields:
  - `name`: Student's name.
  - `timestamp`: Date and time of attendance.
  - `date`: Date for grouping attendance records.

### 3. `Add_new_face.py`
- Provides a GUI for:
  - Adding new students by capturing their photos via webcam.
  - Viewing attendance records stored in MongoDB.
- Updates the `A_model.pkl` file with new encodings.
- Saves student images to the `known_faces` folder.

---

## Usage Notes

1. **Image Requirements:**
   - Ensure images in the `known_faces` folder have clear, frontal faces.
   - Supported formats: `.jpg`, `.png`.

2. **Webcam Requirements:**
   - Ensure the webcam is properly connected and functional.

3. **Attendance Database:**
   - MongoDB should be running for storing attendance records.
   - Default connection string: `mongodb://localhost:27017/`
   - Update the connection string in the scripts if using a remote database.

4. **Student Names:**
   - Names must be unique.
   - Use descriptive filenames for student images (e.g., `John_Doe.jpg`).

---

Thank you