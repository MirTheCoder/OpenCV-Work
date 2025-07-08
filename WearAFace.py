import numpy as np
import cv2
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

hero = cv2.imread("static/clark_2.jpg")
gray_img = cv2.cvtColor(hero, cv2.COLOR_BGR2GRAY)
superman = face_cascade.detectMultiScale(gray_img, 1.3, 5)
for(x,y,w,h) in superman:
    y -= 20
    h += 30
    supermanRect = hero[y:y+h, x:x+w]
    cv2.imwrite("static/superManFace.jpg", supermanRect)

supermanFace = cv2.imread("static/superManFace.jpg")

hero = cv2.imread("static/wonder_woman.jpg")
gray_img = cv2.cvtColor(hero, cv2.COLOR_BGR2GRAY)
wonderWoman = face_cascade.detectMultiScale(gray_img, 1.3, 5)
for(x,y,w,h) in wonderWoman:
    y -= 24
    h += 34
    superWomanRect = hero[y:y+h, x:x+w]
    cv2.imwrite("static/wonderWomanFace.jpg", superWomanRect)

wonderWomanFace = cv2.imread("static/wonderWomanFace.jpg")

letter = 'o'


while True:
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
    faces = face_cascade.detectMultiScale(gray, 1.4, 5)
    #the facial recognition method will return the x,y coordinates along with teh width and height of the rectangle
    #encompassing the face

    if letter == 'o':
        for (x, y, w, h) in faces:
            y -= 30
            x -= 30
            w += 30
            h += 60
            faceCheck = cv2.rectangle(flipped_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)



    if letter == "s":
        for (x, y, w, h) in faces:
            y -= 30
            x -= 30
            w += 30
            h += 60
            faceCheck = cv2.rectangle(flipped_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            dimensions = supermanFace.shape
            superFace = cv2.resize(supermanFace, (w,h))
            flipped_frame[y: y + h, x:x + w] = superFace
            # retrieves the area of the box encapsulating the recognized face
            # Y value goes first before the x value

    if letter == "w":
        for (x, y, w, h) in faces:
            y -= 30
            x -= 30
            w += 30
            h += 60
            faceCheck = cv2.rectangle(flipped_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            superFace = cv2.resize(wonderWomanFace, (w,h))
            flipped_frame[y: y + h, x:x + w] = superFace
            # retrieves the area of the box encapsulating the recognized face
            # Y value goes first before the x value

    #This will store the key that is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        letter = "s"
    elif key == ord("w"):
        letter = 'w'
    elif key == ord("o"):
        letter = "o"
    elif key == ord('q'):
        break




    cv2.imshow('Video Feed', flipped_frame)


cap.release()
cv2.destroyAllWindows()