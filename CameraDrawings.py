import numpy as np
import cv2
import pygame



#This will access the video from your devices camera
#You can also put the file name of a video you want to upload
cap = cv2.VideoCapture(0)
#This wil get the width of our webcam window box, and the nuber three is the identifier of the width property
width = int(cap.get(3)) #rememebr to convert to int because by default the value of cap.get() returns a float number

#This wil get the height of our webcam window box, and the nuber three is the identifier of the height property
height = int(cap.get(4)) #rememebr to convert to int because by default the value of cap.get() returns a float number


letter = 'w'
while True:
    #Here we are getting the frame or actually image being sent by the webcam
    #And then we are also receiving if whether the frame capture was successful
    ret, frame = cap.read()
    #This will flip the frame presented in teh window across the Y axis
    flipped_frame = cv2.flip(frame,1)
    #This is draw a line on our video image
    img = cv2.line(flipped_frame, (0, 0), (width, height), (255, 0, 0), 10)
    img = cv2.line(flipped_frame, (0, height), (width, 0), (255, 0, 0), 10)
    #Pass top left and bottom right coordinates of the rectangle to draw a rectangle
    #To get a solid rectangle, pass -1 in the far right of the cv2.rectangle parameters, else, you just type in a
    #positive number for the thickness of the line
    img = cv2.rectangle(flipped_frame,(100,100), (200,200), (128,128,128), 5)
    img = cv2.circle(flipped_frame, (width//2, height//2), 60, (0,0,255), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #Draw text at bottom left hand corner, this is used to draw text on your image
    img = cv2.putText(flipped_frame, 'Coding is so fun', (10,height-10), font, 2, (0,0,0), 5,  cv2.LINE_AA)

    cv2.imshow('frame', flipped_frame)
    #This is a timer in which our cv2 window will wait according to the time we tell it, and if q is pressed within that
    #time frame then it will not take the picture
    if cv2.waitKey(1) == ord('q'):
        break

#This will release the hold of your webcam
cap.release()
cv2.destroyAllWindows()