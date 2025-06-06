import cv2 as cv
import face_recognition
import pickle as pik
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://face-reognition-8359a-default-rtdb.firebaseio.com/",
    'storageBucket': "face-reognition-8359a.firebasestorage.app"
})

# importing students images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList) 
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)
print(len(imgList))

def findEncodings(imagesList):

    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print('encoding Started')
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
# print("->",encodeListKnown)
print('encoding Compeleted')


file = open("EncodeFile.p", 'wb')
pik.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
