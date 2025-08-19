import numpy as np
import cv2
from deepface import DeepFace



#This will load the required trained XML classifiers that help with face recognition
face_cascade = cv2.CascadeClassifier('video_recog/haarcascade_frontalface_default.xml')
#This will load the required trained XML classifiers that help with eye recognition
eye_cascade = cv2.CascadeClassifier('video_recog/haarcascade_eye.xml')
#This will load the required trained XML classifiers that help with smile recognition
smile_cascade = cv2.CascadeClassifier('video_recog/haarcascade_smile.xml')

#Used to capture the frames or images from a video footage or your devices camera
cap = cv2.VideoCapture(0)

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
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #the facial recognition method will return the x,y coordinates along with teh width and height of the rectangle
    #encompassing the face

    for (x,y,w,h) in faces:
        cv2.rectangle(flipped_frame, (x-30,y-30), (x + w + 30,y + h + 30), (255,0,0), 2 )
        #retrieves the area of the box encapsulating the recognized face
        #Y value goes first before the x value
        region_grey = gray[y:y+h+30, x:x+w+300]
        #This will ensure that we draw the rectangles around the eyes in the colored image
        region_color = flipped_frame[y:y+h+30, x:x+w+30]


        #Detects eyes within the facial recognition area
        eyes = eye_cascade.detectMultiScale(region_grey, 1.3, 5)
        #Detects smile within the facial recognition area
        smile = smile_cascade.detectMultiScale(region_grey, 3.2, 5)

        #For the amount of eyes within the area of the facial recognition, we will draw rectangles around them
        for (ex, ey, ew, eh) in eyes:
            #Draws rectangles on the colored image
            cv2.rectangle(region_color, (ex,ey), (ex + ew , ey + eh), (0,255,0), 2)

        for (sx, sy, sw, sh) in smile:
            # Draws rectangles on the colored image
            cv2.rectangle(region_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)
    cv2.imshow('Video Feed', flipped_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()