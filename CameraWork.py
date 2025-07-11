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
    #This will create a blank canvas that the covers the area of teh webcam window
    image = np.zeros(frame.shape, np.uint8)
    #We want to use this to draw a line on our video image
    #Resizes the frames size
    smaller_frame = cv2.resize(flipped_frame,(fourthWidth,fourthHeight))
    #We use the first line to get a black and white version of our video capture
    gray = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2GRAY)
    #We use this line to get that same color scheme in BGR so that our image will have the required height, width, and channel
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    #Converts our image to a three-dimensional image
    hsv = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2HSV)

    gray_blur = cv2.medianBlur(gray, 5)

    # This will be used to capture the images edges and practically turns it into a binary image by creating a threshold
    # for the pixels values based off the average of the neighboring values, and if a value goes beyond the threshold
    # then it will be turned white, else it will become black
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=9)

    # We use this to smooth the image and make it cleaner while keeping the image sharp, it tells the computer
    # how many colors can be blurred together and how far the image should look for colors to blur

    color = cv2.bilateralFilter(smaller_frame, d=12, sigmaColor=300, sigmaSpace=300)


    gray_color = cv2.bilateralFilter(gray, d=9, sigmaColor=250, sigmaSpace=250)

    # This will blend the edges creation we made with the smoothed out image to create a cartoon like effect
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cartoon2 = cv2.bitwise_and(gray_color, gray_color, mask=edges)

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
        image[:fourthHeight, :fourthWidth] = smaller_frame
        # This paste our frame in the bottom left corner of our webcam window
        image[:fourthHeight, fourthWidth:(2*fourthWidth)] = cv2.rotate(hsv, cv2.ROTATE_180)
        # This paste our frame in the top right corner of our webcam window
        image[:fourthHeight, (2*fourthWidth):(3*fourthWidth)] = cv2.rotate(gray_bgr, cv2.ROTATE_180)
        image[:fourthHeight, (3 * fourthWidth):] = cv2.rotate(gray_bgr, cv2.ROTATE_180)
        # This paste our frame in the bottom right corner of our webcam window
        image[fourthHeight:(2*fourthHeight),:fourthWidth] = cartoon
        # This paste our frame in the bottom left corner of our webcam window
        image[fourthHeight:(2*fourthHeight), fourthWidth:(2 * fourthWidth)] = cv2.rotate(hsv, cv2.ROTATE_180)
        # This paste our frame in the bottom left corner of our webcam window
        image[fourthHeight:(2 * fourthHeight), (2*fourthWidth):(3*fourthWidth)] = cv2.rotate(hsv, cv2.ROTATE_180)
        image[fourthHeight:(2 * fourthHeight), (3 * fourthWidth):] = cv2.rotate(hsv, cv2.ROTATE_180)
        # This paste our frame in the bottom right corner of our webcam window
        image[(2 * fourthHeight):(3 * fourthHeight), :fourthWidth] = cartoon
        # This paste our frame in the bottom left corner of our webcam window
        image[(2 * fourthHeight):(3 * fourthHeight), fourthWidth:(2 * fourthWidth)] = cv2.rotate(hsv, cv2.ROTATE_180)
        # This paste our frame in the bottom left corner of our webcam window
        image[(2 * fourthHeight):(3 * fourthHeight), (2 * fourthWidth):(3*fourthWidth)] = cv2.rotate(hsv, cv2.ROTATE_180)
        image[(2 * fourthHeight):(3 * fourthHeight), (3 * fourthWidth):] = cv2.rotate(hsv, cv2.ROTATE_180)
        image[(3 * fourthHeight):, :fourthWidth] = cv2.rotate(hsv, cv2.ROTATE_180)
        image[(3 * fourthHeight):, fourthWidth: (2 * fourthWidth)] = cv2.rotate(hsv, cv2.ROTATE_180)
        image[(3 * fourthHeight):, (2 * fourthWidth): (3 * fourthWidth)] = cv2.rotate(hsv, cv2.ROTATE_180)
        image[(3 * fourthHeight):, (3 * fourthWidth):] = cv2.rotate(hsv, cv2.ROTATE_180)

    if letter == 'w':
        # This paste our frame in the top left corner of our webcam window
        # img = cv2.line(smaller_frame, (0, 0), (width // 2, height // 2), (255, 0, 0), 10)
        image[:fourthHeight, :fourthWidth] = smaller_frame
        # This paste our frame in the bottom left corner of our webcam window
        image[:fourthHeight, fourthWidth:(2 * fourthWidth)] = hsv
        # This paste our frame in the top right corner of our webcam window
        image[:fourthHeight, (2 * fourthWidth):(3 * fourthWidth)] = gray_bgr
        image[:fourthHeight, (3 * fourthWidth):] = gray_bgr
        # This paste our frame in the bottom right corner of our webcam window
        image[fourthHeight:(2 * fourthHeight), :fourthWidth] = cartoon
        # This paste our frame in the bottom left corner of our webcam window
        image[fourthHeight:(2 * fourthHeight), fourthWidth:(2 * fourthWidth)] = hsv
        # This paste our frame in the bottom left corner of our webcam window
        image[fourthHeight:(2 * fourthHeight), (2 * fourthWidth):(3 * fourthWidth)] = hsv
        image[fourthHeight:(2 * fourthHeight), (3 * fourthWidth):] = hsv
        # This paste our frame in the bottom right corner of our webcam window
        image[(2 * fourthHeight):(3 * fourthHeight), :fourthWidth] = cartoon
        # This paste our frame in the bottom left corner of our webcam window
        image[(2 * fourthHeight):(3 * fourthHeight), fourthWidth:(2 * fourthWidth)] = hsv
        # This paste our frame in the bottom left corner of our webcam window
        image[(2 * fourthHeight):(3 * fourthHeight), (2 * fourthWidth):(3 * fourthWidth)] = hsv
        image[(2 * fourthHeight):(3 * fourthHeight), (3 * fourthWidth):] = hsv
        image[(3 * fourthHeight):, :fourthWidth] = hsv
        image[(3 * fourthHeight):, fourthWidth: (2 * fourthWidth)] = hsv
        image[(3 * fourthHeight):, (2 * fourthWidth): (3 * fourthWidth)] = cartoon
        image[(3 * fourthHeight):, (3 * fourthWidth):] = hsv

    cv2.imshow('frame', image)
    #This is a timer in which our cv2 window will wait according to the time we tell it, and if q is pressed within that
    #time frame then it will not take the picture

#This will release the hold of your webcam
cap.release()
cv2.destroyAllWindows()