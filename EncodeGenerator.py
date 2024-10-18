'''import cv2
import face_recognition
import pickle
import os


def encodeFace():
    # Importing student images
    folderPath = 'Faces'
    pathList = os.listdir(folderPath)
    # print(pathList)
    imgList = []
    studentIds = []
    for path in pathList:
        imgList.append(cv2.imread(os.path.join(folderPath, path)))
        studentIds.append(os.path.splitext(path)[0])
        fileName = f'{folderPath}/{path}'
        # print(path)
        # print(os.path.splitext(path)[0])

    # print(studentIds)

    def findEncodings(imagesList):
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)

        return encodeList

    print("Encoding Started ...")
    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    print("Encoding Complete")

    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print("File Saved")'''
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


