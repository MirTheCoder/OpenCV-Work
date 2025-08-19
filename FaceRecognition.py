import numpy as np
import cv2
from deepface import DeepFace
import os




# Make sure to import Microsoft C++ Redistributable to use tensorflow (an application needed to use DeepFace)
#Make sure your Python interpreter is not beyond 3.11 or else DeeFace will not work




#This will load the required trained XML classifiers that help with face recognition
face_cascade = cv2.CascadeClassifier('video_recog/haarcascade_frontalface_default.xml')
#This will load the required trained XML classifiers that help with eye recognition
eye_cascade = cv2.CascadeClassifier('video_recog/haarcascade_eye.xml')
#This will load the required trained XML classifiers that help with smile recognition
smile_cascade = cv2.CascadeClassifier('video_recog/haarcascade_smile.xml')
#Sets the font for any text that we write
font = cv2.FONT_HERSHEY_SIMPLEX


#Used to capture the frames or images from a video footage or your devices camera
cap = cv2.VideoCapture(0)
#This gets the height of the videocam display box
cameraBoxHeight = int(cap.get(4))
#This gets the width of the videocam display box
cameraBoxWidth = int(cap.get(3))

letter = ''

face = cv2.imread("static/Miracle's headshot.jpeg")


#This function will load the users face into our system as the person we are looking for
def newFace():
    for (x, y, w, h) in faces:
        faceRect = cv2.rectangle(flipped_frame, (x - 30, y - 30), (x + w + 30, y + h + 30), (255, 0, 0), 2)
        faceCheckRect = flipped_frame[y-30: y + h + 30, x-30:x + w + 30 ]



        letter = ''
        path = "static/reference_image.png"
        #We use this to save the cropped image from our video capture to our filepath
        cv2.imwrite(path,faceCheckRect)

while True:
    #Needed in order to keep updating the 'face' if we ever change the image of comparison
    face = "static/reference_image.png"
    ret,frame = cap.read()
    flipped_frame = cv2.flip(frame, 1)
    #You must convert the image to gray scale before you apply the facial detection
    gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
    #This will return the position of all the faces within the image
    #For this we need to put in the image we are applying facial detection to, we need to and a shrinking scale
    #That will shrink the image that you pass into it to ensure that the facial recognition algorithm can work
    #(smaller the value  = high accuracy, slower performance) (bigger the value  = lower accuracy, faster performance)
    #We also need "minNeighbors" which just is our way of letting the algorithm know just how accurate it has to be
    #When it comes to facial recognition because the algorithm can give you all the results it thinks it is a face but
    #some can be inaccurate
    #(Optional)You also have min and maxsize which can determine how small or big the face has to be for facial detection to
    #send it back to you
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #the facial recognition method will return the x,y coordinates along with teh width and height of the rectangle
    #encompassing the face

    for (x, y, w, h) in faces:
        faceCheck = cv2.rectangle(flipped_frame, (x - 30, y - 30), (x + w + 30, y + h + 30), (255, 0, 0), 2)
        faceFrame = flipped_frame[y-30: y + h + 30, x-30:x + w + 30 ]
        # retrieves the area of the box encapsulating the recognized face
        # Y value goes first before the x value

        #This will save the face to an image file to allow the system to compare it with another image in our files
        cv2.imwrite("static/reference_image.png",faceFrame)
        try:
            #Here we are going to load the face we receive from the video capture and the face that we are
            #going to be comparing it to from our files
            facial = cv2.imread("static/reference_image.png")
            #This will allow us to compare the cropped face images in the video footage and compare them
            #enforce_detection allows us to compare faceFrame with face since faceFrame is actually a numpy array
            match = DeepFace.verify(facial,face, enforce_detection=False)
            #Since DeepFace returns a dictionary answer with the True or False value being stored in "['verified']", we have
            #to check and see if the verified value in the dictionary is equal to True
            if match['verified']:
                cv2.putText(flipped_frame, 'Welcome Back', (10, cameraBoxHeight - 10), font, 2, (0, 0, 0), 5, cv2.LINE_AA)
            else:
                cv2.putText(flipped_frame, 'Do I know you?', (10, cameraBoxHeight - 10), font, 2, (0, 0, 0), 5, cv2.LINE_AA)
        except Exception as e:
            print("Error: ", e)

    #This will store the key that is pressed
    key = cv2.waitKey(1) & 0xFF

    if key == ord('n'):
        letter = 'n'
    elif key == ord('w'):
        letter = 'w'
    elif key == ord('q'):
        break

    if letter == 'n':
       newFace()



    cv2.imshow('Video Feed', flipped_frame)


cap.release()
cv2.destroyAllWindows()