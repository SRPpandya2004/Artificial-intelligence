import os

import cv2
import cv2 as cv
import pickle

import cvzone
import face_recognition
import numpy as np
import cvzone as cvz

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

from datetime import datetime
from datetime import date

import openpyxl
from xlwt import Workbook
import xlwt
from xlutils.copy import copy as xl_copy

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-reognition-8359a-default-rtdb.firebaseio.com/",
    'storageBucket': "face-reognition-8359a.firebasestorage.app"
})

bucket = storage.bucket()

cap = cv.VideoCapture(0)

# setting the height and width od the webcam
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

imageBackground = cv.imread('Resources/background.png')

# importing the mode images to the list
folderModepath = 'Resources/Modes'
modes_path = os.listdir(folderModepath)
modeImage_List = []

# appending path to the modeImage_List list
for path in modes_path:
    modeImage_List.append(cv.imread(os.path.join(folderModepath, path)))

# load the encode files
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)

modeType = 0
# for mode type
counter = 0
id = -1
imgStudent = []

row=1
col=0
already_attendence_taken = ""

while True:
    isTrue, video_cap = cap.read()

    # scaling image to 1/4th of it's size
    imgS = cv.resize(video_cap, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

    imageBackground[162:162 + 480, 55:55 + 640] = video_cap
    imageBackground[44:44 + 633, 808:808 + 414] = modeImage_List[modeType]

    if faceCurrentFrame:

        for ef, fl in zip(encodeCurrentFrame, faceCurrentFrame):  # ef:encode face and fl: face lock
            matches = face_recognition.compare_faces(encodeListKnown, ef)
            face_distance = face_recognition.face_distance(encodeListKnown, ef)
            # print('matches', matches)
            # print('face_distance', face_distance)
            matchIndex = np.argmin(face_distance)
            # print(matchIndex)

            if matches[matchIndex]:

                # print('Face Detected')
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = fl
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                cvz.cornerRect(
                    imageBackground,  # The image to draw on
                    (55 + x1, 162 + y1, x2 - x1, y2 - y1),
                    # The position and dimensions of the rectangle (x, y, width, height)
                    l=35,  # Length of the corner edges
                    t=5,  # Thickness of the corner edges
                    rt=1,  # Thickness of the rectangle
                    colorR=(255, 0, 255),  # Color of the rectangle
                    colorC=(0, 255, 0)  # Color of the corner edges
                )
                id = studentIds[matchIndex]

                # print(id)
                if counter == 0:
                    # for loading animation
                    cvzone.putTextRect(imageBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imageBackground)
                    cv.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # Get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv.imdecode(array, cv.COLOR_BGRA2BGR)

                # update data of attendance

                datetimeObj = datetime.strptime(studentInfo["last_attendance"], "%d-%m-%Y %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObj).total_seconds()
                print(secondsElapsed)

                if secondsElapsed > 60:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance').set(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imageBackground[44:44 + 633, 808:808 + 414] = modeImage_List[modeType]

            if modeType != 3:

                if 5 < counter <= 10:
                    modeType = 2

                imageBackground[44:44 + 633, 808:808 + 414] = modeImage_List[modeType]



                if counter <= 5:
                    # total_attendance
                    cv.putText(imageBackground, str(studentInfo['total_attendance']), (861, 125),
                               cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                    # Name
                    (w, h), _ = cv.getTextSize(studentInfo['Name'], cv.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv.putText(imageBackground, str(studentInfo['Name']), (808 + offset, 445),
                               cv.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    # Major
                    cv.putText(imageBackground, str(studentInfo['Major']), (1006, 550),
                               cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    # id
                    cv.putText(imageBackground, str(id), (1006, 493),
                               cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    #Standing
                    cv.putText(imageBackground, str(studentInfo['Standing']), (910, 625),
                               cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    #Year
                    cv.putText(imageBackground, str(studentInfo['year']), (1025, 625),
                               cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    #starting_year
                    cv.putText(imageBackground, str(studentInfo['starting_year']), (1125, 625),
                               cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    imageBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 10:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imageBackground[44:44 + 633, 808:808 + 414] = modeImage_List[modeType]

    else:
        modeType = 0
        counter = 0

    #cv.imshow('face_recognition', video_cap)
    cv.imshow("Face Attendance", imageBackground)

    if cv.waitKey(20) & 0xFF == ord('b'):
        break


# 10-01-2005 00:54:34 date time format
