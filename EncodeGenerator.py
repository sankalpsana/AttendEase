import cv2
import face_recognition
import pickle
import os

from attendanceTool import add_student_to_all_sheets


# Load existing encodings from the file (if any)
def load_encodings():
    if os.path.exists("EncodeFile.p"):
        with open("EncodeFile.p", 'rb') as file:
            encodeListKnownWithIds = pickle.load(file)
        return encodeListKnownWithIds[0], encodeListKnownWithIds[1]  # encodings and student IDs
    else:
        return [], []  # Return empty lists if no encodings exist yet

# Function to add a new face encoding for a given image path and student ID
def add_face_encoding(imagePath, studentId):
    # Load existing encodings
    encodeListKnown, studentIdsKnown = load_encodings()

    # Check if student ID already exists
    if studentId in studentIdsKnown:
        print(f"Student ID {studentId} already exists in the encoding file.")
        return

    # Read the image and process it
    img = cv2.imread(imagePath)
    if img is None:
        print(f"Error: Could not read image from {imagePath}")
        return

    # Convert the image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Encode the face from the image
    try:
        encode = face_recognition.face_encodings(img)[0]
    except IndexError:
        print("No face detected in the image. Encoding not added.")
        return

    # Add the new encoding and student ID to the lists
    encodeListKnown.append(encode)
    studentIdsKnown.append(studentId)

    # Save the updated encodings back to the file
    encodeListKnownWithIds = [encodeListKnown, studentIdsKnown]
    with open("EncodeFile.p", 'wb') as file:
        pickle.dump(encodeListKnownWithIds, file)

    add_student_to_all_sheets(studentId)
    print(f"Face encoding for Student ID {studentId} added successfully.")

def delete_face_encoding(studentId):
    # Load existing encodings and IDs
    encodeListKnown, studentIdsKnown = load_encodings()

    # Check if student ID exists
    if studentId not in studentIdsKnown:
        print(f"Student ID {studentId} does not exist in the encoding file.")
        return

    # Find the index of the student ID and remove the encoding and ID
    index = studentIdsKnown.index(studentId)
    del encodeListKnown[index]
    del studentIdsKnown[index]

    # Save the updated encodings and IDs back to the file
    encodeListKnownWithIds = [encodeListKnown, studentIdsKnown]
    with open("EncodeFile.p", 'wb') as file:
        pickle.dump(encodeListKnownWithIds, file)

    print(f"Face encoding for Student ID {studentId} deleted successfully.")

#delete_face_encoding('2002')