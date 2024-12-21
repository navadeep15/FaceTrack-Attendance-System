import os
import pickle
import cv2
import numpy as np
import face_recognition
from datetime import datetime
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["attendance_system"]  # Database name
collection = db["attendance_records"]  # Attendance collection

# Load the face encodings and names
model_file = "A_model.pkl"
if not os.path.exists(model_file):
    print("Model file not found! Ensure you add students first.")
    exit()

with open(model_file, "rb") as file:
    data = pickle.load(file)
    known_encodings = data["encodings"]
    known_names = data["names"]

print("Model loaded successfully.")
print("Press 'q' to quit and save attendance.")

# Open webcam
video_capture = cv2.VideoCapture(0)

try:
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the frame to RGB
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all face locations in the frame
        face_locations = face_recognition.face_locations(rgb_small_frame)

        # Encode the faces found
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Process each detected face
        for face_encoding in face_encodings:
            # Compare the face encoding with known encodings
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            name = "Unknown"
            if True in matches:
                # Get the index of the best match
                best_match_index = np.argmin(face_distances)
                name = known_names[best_match_index]

                # Check if the name is already recorded in the database for today
                current_date = datetime.now().strftime("%Y-%m-%d")
                existing_record = collection.find_one({"name": name, "date": current_date})

                if not existing_record:
                    # Insert new attendance record
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    attendance_record = {
                        "name": name,
                        "timestamp": timestamp,
                        "date": current_date  # To group attendance by day
                    }
                    collection.insert_one(attendance_record)
                    print(f"Attendance marked: {name} at {timestamp}")
                else:
                    print(f"Attendance already recorded for {name} today.")

            # Display the frame with rectangles around detected faces
            for (top, right, bottom, left) in face_locations:
                # Scale back up the face locations since the frame was scaled down
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # Display the name below the rectangle
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Display the resulting frame
        cv2.imshow("Video", frame)

        # Quit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

except KeyboardInterrupt:
    print("\nProgram interrupted manually. Exiting...")
finally:
    # Release the webcam and close windows
    video_capture.release()
    cv2.destroyAllWindows()
    print("Resources released. Program terminated.")
