import numpy as np
import cv2



#This will access the video from your devices camera
#You can also put the file name of a video you want to upload
cap = cv2.VideoCapture(0)
#This wil get the width of our webcam window box, and the nuber three is the identifier of the width property
width = int(cap.get(3)) #rememebr to convert to int because by default the value of cap.get() returns a float number
fourthWidth = width//4

#This wil get the height of our webcam window box, and the nuber three is the identifier of the height property
height = int(cap.get(4)) #rememebr to convert to int because by default the value of cap.get() returns a float number
fourthHeight = height//4


letter = 'w'
while True:
    #Here we are getting the frame or actually image being sent by the webcam
    #And then we are also receiving if whether the frame capture was successful
    ret, frame = cap.read()
    #This will flip the frame presented in teh window across the Y axis
    flipped_frame = cv2.flip(frame,1)
    #We want to use this to draw a line on our video image
    #Resizes the frames size
    smaller_frame = cv2.resize(flipped_frame,(fourthWidth,fourthHeight))
    #We use the first line to get a black and white version of our video capture
    gray = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2GRAY)
    th, dst = cv2.threshold(gray, 200, 255,
                                cv2.THRESH_BINARY) #cv2.thresh_binary helps convert our image to BGR with respect to the threshold limits we gave/added

    # We use this to smooth the image and make it cleaner while keeping the image sharp, it tells the computer
    # how many colors can be blurred together and how far the image should look for colors to blur

    #This takes a section of our video webcam window and paste the smaller frame into it

    key = cv2.waitKey(1) & 0xFF

    if key == ord('d'):
        letter = 'd'
    elif key == ord('w'):
        letter = 'w'
    elif key == ord('q'):
        break

    cv2.imshow('frame', dst)
    #This is a timer in which our cv2 window will wait according to the time we tell it, and if q is pressed within that
    #time frame then it will not take the picture

#This will release the hold of your webcam
cap.release()
cv2.destroyAllWindows()