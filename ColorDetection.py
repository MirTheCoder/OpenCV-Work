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
    #Used to edit how our colors are displayed on our webcam. (In this case we will be going from BGR to HSV color display)
    hsv = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2HSV)

    #This will create the boundary for the colors that our webcam will show
    lower_blue = np.array([0,70,50])
    upper_blue = np.array([179,50,255])

    #This will mask our webcam so that only the colors within our color range are shown
    mask = cv2.inRange(hsv,lower_blue,upper_blue)

    #This is used to compare the image in order for the mask to determine which pixels must be blacked out in order to
    #keep only the blue pixels
    result = cv2.bitwise_and(flipped_frame, flipped_frame, mask=mask)

    #This will display the image with the edited color scheme
    cv2.imshow('frame', result)
    #This is a timer in which our cv2 window will wait according to the time we tell it, and if q is pressed within that
    #time frame then it will not take the picture
    if cv2.waitKey(1) == ord('q'):
        break

#This will release the hold of your webcam
cap.release()
cv2.destroyAllWindows()


