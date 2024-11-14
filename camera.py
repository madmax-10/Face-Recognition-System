from cv2 import VideoCapture,flip,putText,imshow,waitKey,COLOR_BGR2RGB,destroyWindow,rectangle,resize,cvtColor,FONT_HERSHEY_COMPLEX, FONT_HERSHEY_PLAIN
from face_recognition import face_locations,face_encodings,face_distance,compare_faces
from time import time
from pickle import dump,load
from numpy import argmin

class Camera():

    def start(self,liveRecog, newUser,id=None,name=None):

        knownIDs,knownEncodings,knownNames=self.loadData()
        a=True
        pTime=0
        cam = VideoCapture(0)       
        framePhoto = None

        while True:

            success, frameVideo = cam.read()
            frameVideo=flip(frameVideo,1)
            framePhoto = frameVideo.copy()   

            if a:
                locs,frame=self.faceLocations(frameVideo)

                if liveRecog:
                    names,confidences=self.detectPerson(self.faceEncodings(frame,locs),knownIDs,knownEncodings,knownNames)  

            a = not a

            if not liveRecog:
                self.drawRectangle(frameVideo,locs)

            elif liveRecog:
                self.annotate(frameVideo,locs,names,confidences)
                cTime = time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                putText(frameVideo, f'FPS: {int(fps)}', (20, 70), FONT_HERSHEY_PLAIN,3, (0, 255, 0), 2)

            imshow("Video",frameVideo)

            if waitKey(1) & 0xFF==ord('c'):    
                destroyWindow("Video")
                break

        cam.release()

        if not liveRecog:
            faceLocs,processedPhoto=self.faceLocations(framePhoto)

            if newUser:
                self.addUser(self.faceEncodings(processedPhoto,faceLocs),id,name)
            else:  
                return self.detectPerson(self.faceEncodings(processedPhoto,faceLocs),knownIDs,knownEncodings,knownNames)[0]

    def faceLocations(self,frame):

        frameInput=resize(frame,(0,0),None,0.25,0.25)
        frameInput=cvtColor(frameInput,COLOR_BGR2RGB)
        faceLocs=face_locations(frameInput)
        list=[faceLocs,frameInput]

        return list
    
    def faceEncodings(self,frame,locs):
        return face_encodings(frame,locs)
    
    def loadData(self):

        knownIDs=[]
        knownEncodings=[]
        with open("knownEncodings.pkl","rb") as f:
            while True:
                try:
                    knownEncodingsWithIDs=load(f)
                    knownIDs.extend(list(knownEncodingsWithIDs.keys()))
                    knownEncodings.extend(list(knownEncodingsWithIDs.values()))
                except EOFError:
                    break

        knownNames={}
        with open("knownIDs.pkl","rb") as f:
                    while True:
                        try:
                            knownNames.update(load(f))
                        except EOFError:
                            break

        return [knownIDs,knownEncodings,knownNames]     

    def drawRectangle(self,frame,locs):

        for (y1,x2,y2,x1) in locs:
            x1*=4
            y1*=4
            x2*=4
            y2*=4
            return rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
    
    def annotate(self,frame,locs,names,confidences):

        for (y1,x2,y2,x1),name,confidence in zip(locs,names,confidences):
            x1*=4
            y1*=4
            x2*=4
            y2*=4
            rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
            rectangle(frame,(x1,y2-35),(x2,y2),(255,0,0),-1)
            putText(frame,f"{name}({confidence})",(x1+6,y2-6),FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    def calculateConfidence(self,facedis):
        return int((1-float(facedis))*100)

    def detectPerson(self,faceEncodings,knownIDs,knownEncodings,knownNames):

        recognizedNames=[]
        confidences=[]
        print(len(faceEncodings))
        print(len(knownEncodings))
        if (len(faceEncodings)<1 or len(knownEncodings)<1):
            return [recognizedNames,confidences]
            
        for face in faceEncodings:
            matches=compare_faces(knownEncodings,face)
            faceDis=face_distance(knownEncodings,face)
            matchIndex=argmin(faceDis)
            if matches[matchIndex]:
                id = knownIDs[matchIndex]  
                name = knownNames[id]
                conf= self.calculateConfidence(faceDis[matchIndex])
                if(conf>=50):
                    recognizedNames.append(name)
                    confidences.append(conf)

        return [recognizedNames,confidences]
                        
    def addUser(self, faceEncodings, IDs, names):
        
        if len(faceEncodings)>0:
            if len(IDs)==len(faceEncodings):
                knownEncodingsWithIDs={}
                for faceEncoding, UID in zip(faceEncodings,IDs):
                    knownEncodingsWithIDs[UID]=faceEncoding
                with open("knownEncodings.pkl","ab") as f:
                    dump(knownEncodingsWithIDs,f)
                knownIDs={}
                for UID, name in zip(IDs,names):
                    knownIDs[UID]=name
                with open("knownIDs.pkl","ab") as f:
                    dump(knownIDs,f)