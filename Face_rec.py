import os
import pickle
import numpy as np
import cv2
import face_recognition
import numpy as np
from datetime import datetime
from attendanceTool import mark_attendance

def recProcess(date, subject):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # Importing the mode images into a list

    imgModeList = []
    # print(len(imgModeList))

    # Load the encoding file
    print("Loading Encode File ...")
    file = open('EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    # print(studentIds)
    print("Encode File Loaded")

    modeType = 0
    counter = 0
    id = -1
    imgStudent = []
    presentToday = []
    #date = "14-10-2024"
    #subject = 'Sheet1'
    file_path = "attendance.xlsx"

    while True:
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print("matches", matches)
                # print("faceDis", faceDis)

                matchIndex = np.argmin(faceDis)
                # print("Match Index", matchIndex)

                if matches[matchIndex]:
                    # print("Known Face Detected")
                    # print(studentIds[matchIndex])
                    top, right, bottom, left = faceLoc
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    id = studentIds[matchIndex]
                    cv2.putText(img, id, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    if counter == 0:
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1

            if counter != 0:

                if counter == 1:
                    # Get the Data

                    # Update data of attendance

                    if id not in presentToday:
                        presentToday.append(id)
                        mark_attendance(id, date, 'present', file_path, subject)
                    else:
                        modeType = 3
                        counter = 0

                if modeType != 3:

                    if 10 < counter < 20:
                        modeType = 2

                    if counter <= 10:
                        print("Marked")
                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
        else:
            modeType = 0
            counter = 0
        # cv2.imshow("Webcam", img)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
