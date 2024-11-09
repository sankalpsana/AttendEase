import base64
import os
import pickle
from datetime import time
import numpy as np
from io import BytesIO
from PIL import Image
from flask import Flask, render_template,  request, jsonify
import cv2
import face_recognition
from EncodeGenerator import add_face_encoding
from attendanceTool import  mark_attendance
from pyngrok import ngrok

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture():
    return render_template('capture.html')


@app.route('/attendance_form')
def attendance_form():
    return render_template('attendance_form.html')

@app.route('/attendance_capture')
def attendance_capture():
    return render_template('attendance_capture.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    try:
        with open('EncodeFile.p', 'rb') as file:
            known_encodings_with_ids = pickle.load(file)
        known_encodings = known_encodings_with_ids[0]
        student_ids = known_encodings_with_ids[1]
        print(student_ids)
    except FileNotFoundError:
        known_encodings = []
        student_ids = []
    data = request.get_json()

    # Extract image data from the JSON payload
    image_data = data['image']
    date = data.get('date')
    subject = data.get('subject')

    # Decode base64 image data
    image_data = image_data.split(",")[1]  # Remove the "data:image/jpeg;base64," part
    image = base64.b64decode(image_data)

    # Convert the image to a numpy array
    np_image = np.frombuffer(image, dtype=np.uint8)

    # Decode the numpy array as an image using OpenCV
    img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Detect faces in the image
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    faces_info = []

    # Compare each face encoding with known encodings
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)

        # If a match is found, get the student ID
        if True in matches:
            best_match_index = np.argmin(face_distances)
            student_id = student_ids[best_match_index]
            print(f'{student_id} found')

        # Append face location and student ID to results
        faces_info.append({
            "location": face_location,  # [top, right, bottom, left]
            "student_id": student_id
        })

    # Return the face locations and student IDs as a response
    return jsonify({
        "faces": faces_info,
        "message": f"Processed {len(face_locations)} face(s)"
    })

@app.route('/stop_attendance', methods=['POST'])
def stop_attendance():
    data = request.get_json()
    detected_students = data.get('student_ids', [])
    date_str = data.get('date')
    sheet_name = data.get('subject')

    if detected_students and date_str and sheet_name:
        mark_attendance(detected_students, 'present', date_str, sheet_name)
        return jsonify({"message": "Attendance updated successfully"}), 200
    else:
        return jsonify({"message": "Missing data for attendance marking"}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    image_data = data['image']
    studentid = data['student_id']

    # Decode the Base64 image
    image_data = image_data.split(",")[1]
    image_decoded = base64.b64decode(image_data)

    # Convert the decoded image to an OpenCV image
    image = Image.open(BytesIO(image_decoded))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image_filename = f"{studentid}.jpg"

    # Save the file
    cv2.imwrite(image_filename, image)

    #Process Image
    image = cv2.imread(image_filename)
    # Convert the image to grayscale (Haar Cascade works better on grayscale images)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If a face is detected
    if len(faces) > 0:
        # Get the coordinates of the first detected face (x, y, w, h)
        x, y, w, h = faces[0]

        # Crop the image to include only the face
        face_image = image[y:y + h, x:x + w]

        # Save the cropped face image
        crop_file_name = f"{studentid}.jpg"

        # Path where you want to save the cropped image
        cropped_image_path = os.path.join('Faces', crop_file_name)
        cv2.imwrite(cropped_image_path, face_image)
        os.remove(image_filename)

        add_face_encoding(cropped_image_path,studentid)

        print("Image uploaded successfully!")

        # Redirect to the index page
        return jsonify({"status": "success", "message": f"Photo for student {studentid} saved!"})


'''if __name__ == "__main__":'''
public_url = ngrok.connect(name='flask').public_url
print(" * ngrok URL: " + public_url + " *")
app.run()