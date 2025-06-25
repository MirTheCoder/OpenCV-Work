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
    #This will create a blank canvas that the covers the area of teh webcam window
    image = np.zeros(frame.shape, np.uint8)
    #Resizes the frames size
    smaller_frame = cv2.resize(frame,(0,0), fx=0.5, fy=0.5)
    #This takes a section of our video webcam window and paste the smaller frame into it

    if cv2.waitKey(1) == ord('d'):
        letter = 'd'

    if cv2.waitKey(1) == ord('w'):
        letter = 'w'

    if letter == 'd':
        #This paste our frame in the top left corner of our webcam window
        image[:height//2, :width//2] = smaller_frame
        # This paste our frame in the bottom left corner of our webcam window
        image[height // 2:, :width // 2] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
        # This paste our frame in the top right corner of our webcam window
        image[:height // 2, width // 2:] = smaller_frame
        # This paste our frame in the bottom right corner of our webcam window
        image[height // 2:, width // 2:] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
    if letter == 'w':
        #This paste our frame in the top left corner of our webcam window
        image[:height//2, :width//2] = smaller_frame
        # This paste our frame in the bottom left corner of our webcam window
        image[height // 2:, :width // 2] = smaller_frame
        # This paste our frame in the top right corner of our webcam window
        image[:height // 2, width // 2:] = smaller_frame
        # This paste our frame in the bottom right corner of our webcam window
        image[height // 2:, width // 2:] = smaller_frame

    cv2.imshow('frame', image)
    #This is a timer in which our cv2 window will wait according to the time we tell it, and if q is pressed within that
    #time frame then it will not take the picture
    if cv2.waitKey(1) == ord('q'):
        break

#This will release the hold of your webcam
cap.release()
cv2.destroyAllWindows()