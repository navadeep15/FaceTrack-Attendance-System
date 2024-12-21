import os
import face_recognition
import pickle

# Directory containing student images
students_dir = "known_faces"

# Dictionary to hold encodings and names
students_encodings = []
students_names = []

# Process each student's image
for student_image in os.listdir(students_dir):
    if student_image.endswith(('.jpg', '.png')):
        image_path = os.path.join(students_dir, student_image)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)

        if encoding:  # Ensure the face is detected
            students_encodings.append(encoding[0])
            students_names.append(os.path.splitext(student_image)[0])

# Save the encodings and names
model_file = "A_model.pkl"
with open(model_file, "wb") as file:
    pickle.dump({"encodings": students_encodings, "names": students_names}, file)

print(f"Model saved to {model_file}")
