import numpy as np
import cv2



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
    #We want to use this to draw a line on our video image
    #Resizes the frames size
    smaller_frame = cv2.resize(flipped_frame,(0,0), fx=0.5, fy=0.5)
    #We use the first line to get a black and white version of our video capture
    gray = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2GRAY)
    #We use this line to get that same color scheme in BGR so that our image will have the required height, width, and channel
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    #Converts our image to a three-dimensional image
    hsv = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2HSV)
    #This takes a section of our video webcam window and paste the smaller frame into it

    key = cv2.waitKey(1) & 0xFF

    if key == ord('d'):
        letter = 'd'
    elif key == ord('w'):
        letter = 'w'
    elif key == ord('q'):
        break

    if letter == 'd':
        #This paste our frame in the top left corner of our webcam window
        #img = cv2.line(smaller_frame, (0, 0), (width // 2, height // 2), (255, 0, 0), 10)
        image[:height//2, :width//2] = smaller_frame
        # This paste our frame in the bottom left corner of our webcam window
        image[height // 2:, :width // 2] = cv2.rotate(hsv, cv2.ROTATE_180)
        # This paste our frame in the top right corner of our webcam window
        image[:height // 2, width // 2:] = cv2.rotate(gray_bgr, cv2.ROTATE_180)
        # This paste our frame in the bottom right corner of our webcam window
        image[height // 2:, width // 2:] = smaller_frame
    if letter == 'w':
        #img = cv2.line(smaller_frame, (0, 0), (width // 2, height // 2), (255, 0, 0), 10)
        #This paste our frame in the top left corner of our webcam window
        image[:height//2, :width//2] = smaller_frame
        # This paste our frame in the bottom left corner of our webcam window
        image[height // 2:, :width // 2] = hsv
        # This paste our frame in the top right corner of our webcam window
        image[:height // 2, width // 2:] = gray_bgr
        # This paste our frame in the bottom right corner of our webcam window
        image[height // 2:, width // 2:] = smaller_frame

    cv2.imshow('frame', image)
    #This is a timer in which our cv2 window will wait according to the time we tell it, and if q is pressed within that
    #time frame then it will not take the picture

#This will release the hold of your webcam
cap.release()
cv2.destroyAllWindows()