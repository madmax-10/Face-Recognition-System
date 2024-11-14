# Run this program before running main.py the very first time

import os
import cv2
import face_recognition
import pickle
knownPhotos=os.listdir("Photos")
knownEncodingsWithIDs={}
for knPh in knownPhotos:
    knownID=os.path.splitext(knPh)[0]
    img=cv2.imread(f"Photos/{knPh}")
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    faceLocs=face_recognition.face_locations(imgRGB)
    faceEncode=face_recognition.face_encodings(imgRGB,faceLocs)[0]
    knownEncodingsWithIDs.update({knownID:faceEncode})
with open("knownEncodings.pkl","wb") as fileEncodes:
    pickle.dump(knownEncodingsWithIDs,fileEncodes)