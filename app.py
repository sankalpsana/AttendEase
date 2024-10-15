import base64
import os
from asyncio import wait_for
import numpy as np
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, Response, request,redirect,url_for,jsonify
import cv2
import face_recognition
from Face_rec import recProcess
from EncodeGenerator import encodeFace
from attendanceTool import add_student_to_all_sheets

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        if not success:
            break
        else:

            face_locations = face_recognition.face_locations(imgS)

            for (top, right, bottom, left) in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)




            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture():
    return render_template('capture.html')

'''@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')'''


@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    image_data = data['image']
    student_id = data['student_id']

    # Decode the Base64 image
    image_data = image_data.split(",")[1]
    image_decoded = base64.b64decode(image_data)

    # Convert the decoded image to an OpenCV image
    image = Image.open(BytesIO(image_decoded))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image_filename = f"{student_id}.jpg"

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
        crop_file_name = f"{student_id}.jpg"

        # Path where you want to save the cropped image
        cropped_image_path = os.path.join('Faces', crop_file_name)
        cv2.imwrite(cropped_image_path, face_image)
        os.remove(image_filename)
        encodeFace()
        add_student_to_all_sheets(student_id, 'attendance.xlsx')
        print("Image uploaded successfully!")

        # Redirect to the index page
        return jsonify({"status": "success", "message": f"Photo for student {student_id} saved!"})

@app.route('/video_feed/<date>/<subject>')
def video_feed(date, subject):
    return Response(recProcess(date, subject), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(debug=True)
