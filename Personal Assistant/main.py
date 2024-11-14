import pyttsx3
import speech_recognition as sr
from camera import Camera
from text2digits import text2digits

def speak(command):
    speaker.say(command)
    speaker.runAndWait()

def read():
    with open("AdminInfos.txt","r") as f:
        data=f.read()
    pswd = data.split("\n")[0]
    currId = int(data.split("\n")[1])
    return[pswd,currId]

def write(pswd,currId):
    with open("AdminInfos.txt","w") as f:
        f.write(f"{pswd}\n{currId}")

def verifyUser():    
    speak("First, I need to verify your identity. After some time, camera will open. Please click C when you wish to take the photo for your Identification.")
    names = c.start(False,False)
    if len(names)>0:
        for user in names:
            speak(f"Hi {user}")
        liveRecog()
    else:
        askForAdmission()

def askForAdmission():
    speak("I couldn't recognize anyone in the frame. Do you want to add your profile?")
    if takeCommand() == "yes":
        addUser()
    elif takeCommand() == "no":
        speak("Sorry! but there needs to be someone I recognize. Please try again!")
        verifyUser()
    else:
        speak("Sorry")
        askForAdmission()

def addUser():
    speak("Please tell, how many profiles do you want to create? I meant, how many people? Say the number")
    names=[]
    ids=[]
    for i in range (0,int(t2d.convert(takeCommand()))):
        pswd,currId=read()
        currId=int(currId)+1
        write(pswd,currId)
        ids.append(currId)
        speak("Please enter the name.")
        names.append(input())

    c.start(False,True,ids,names)
    liveRecog()

def liveRecog():
    c.start(True,False)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 0.6
        audio = r.listen(source)
    try:
        print("Recognizing...")
        q = r.recognize_google(audio,language='en-in')
        print(f"You said: {q}")
        return q
    except:
        print("Couldn't recognize....!!")
        takeCommand()

if __name__=="__main__":
    speaker = pyttsx3.init()
    speaker.setProperty('voice',"com.apple.eloquence.en-US.Eddy")
    c=Camera()
    t2d = text2digits.Text2Digits()    
    speak("Hello, I am Madmax, a personal assistant created by Mr. Ashkal Bhattarai.")
    verifyUser()