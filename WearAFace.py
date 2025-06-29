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

img = cv2.imread("static/clark_2.jpg")
img = cv2.resize(img,(cameraBoxWidth, cameraBoxHeight))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
superman = face_cascade.detectMultiScale(gray_img, 1.3, 5)
sx,sy,sw,sh = superman[0]
sx = int(sx)
sy = int(sy)
sw = int(sw)
sh = int(sh)

supermanFace = img[sy - 30: sy + sh + 30, sx - 30:sx + sw + 30]


letter = ''

faceFrame = img
face = "static/reference_image.png"


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
        supermanFace = cv2.resize(supermanFace, (x+x+w,y+y+w))
        flipped_frame[y-30: y + h + 30, x-30:x + w + 30 ] = supermanFace
        # retrieves the area of the box encapsulating the recognized face
        # Y value goes first before the x value

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