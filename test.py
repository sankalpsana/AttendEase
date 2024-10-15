import cv2
from flask import Flask, request, render_template

# Load the pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Load the input image
#input_image_path = 'Faces/Sankalp/sankalp1.jpg'  # Replace with your image path
image = cv2.imread(input_image_path)

# Convert the image to grayscale (Haar Cascade works better on grayscale images)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# If a face is detected
if len(faces) > 0:
    # Get the coordinates of the first detected face (x, y, w, h)
    x, y, w, h = faces[0]

    # Crop the image to include only the face
    face_image = image[y:y+h, x:x+w]

    # Save the cropped face image
    cropped_image_path = 'cropped_face.jpg'  # Path where you want to save the cropped image
    cv2.imwrite(cropped_image_path, face_image)

    # Optionally display the cropped face image
    '''cv2.imshow('Cropped Face', face_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
else:
    print("No face detected in the image.")
