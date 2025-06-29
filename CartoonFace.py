import numpy as np
import cv2




#This will load the required trained XML classifiers that help with face recognition
face_cascade = cv2.CascadeClassifier('video_recog/haarcascade_frontalface_default.xml')
#This will load the required trained XML classifiers that help with eye recognition
eye_cascade = cv2.CascadeClassifier('video_recog/haarcascade_eye.xml')
#This will load the required trained XML classifiers that help with smile recognition
smile_cascade = cv2.CascadeClassifier('video_recog/haarcascade_smile.xml')

#Used to capture the frames or images from a video footage or your devices camera
cap = cv2.VideoCapture(0)
letter = 'a'


while True:
    ret,frame = cap.read()
    flipped_frame = cv2.flip(frame, 1)
    original = flipped_frame
    #You must convert the image to gray scale before you apply the facial detection
    gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
    #gray_height = gray.get(4)
    #gray_width = gray.get(3)
    #This will return the position of all the faces within the image
    #For this we need to put in the image we are applying facial detection to, we need to and a shrinking scale
    #That will shrink the image that you pass into it to ensure that the facial recognition algorithm can work
    #(smaller the value  = high accuracy, slower performance) (bigger the value  = lower accuracy, faster performance)
    #We also need "minNeighbors" which just is our way of letting the algorithm know just how accurate it has to be
    #When it comes to facial recognition because the algorithm can give you all the results it thinks it is a face but
    #some can be inaccurate
    #(Optional)You also have min and maxsize which can determine how small or big the face has to be for facial detection to
    #send it back to you
    faces = face_cascade.detectMultiScale(gray, 1.8, 5)
    #the facial recognition method will return the x,y coordinates along with teh width and height of the rectangle
    #encompassing the face
    if letter == 'a':
        for (x,y,w,h) in faces:
            x = x - 50
            y = y - 50
            w = w + 80
            h = h + 80

            if letter == 'a': #We will put a different if statement here that deals with the video box boundaries
                cv2.rectangle(flipped_frame, (x,y), (x + w,y + h), (255,0,0), 2 )
                #retrieves the area of the box encapsulating the recognized face
                #Y value goes first before the x value
                region_grey = gray[y:y+h, x:x+w]
                #This will ensure that we draw the rectangles around the eyes in the colored image
                region_color = flipped_frame[y:y+h, x:x+w]

                #This helps to remove noise from an image by altering the values of pixels based off of the median value when
                #you factor in values of the pixels neighboring it. (The neighborhood of pixels included in each median blur is
                #determined by the kernel size which in this case if 5 and thus calls for a 5x5 box as the neighborhood of
                #pixel values to factor in to get the median value. Also makes capturing edges of an image easier
                gray_blur = cv2.medianBlur(region_grey, 5)

                #This will be used to capture the images edges and practically turns it into a binary image by creating a threshold
                #for the pixels values based off the average of the neighboring values, and if a value goes beyond the threshold
                #then it will be turned white, else it will become black
                edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,blockSize=9, C=9)

                #We use this to smooth the image and make it cleaner while keeping the image sharp, it tells the computer
                #how many colors can be blurred together and how far the image should look for colors to blur
                color = cv2.bilateralFilter(region_color, d=15, sigmaColor=650, sigmaSpace=650)

                #This will blend the edges creation we made with the smoothed out image to create a cartoon like effect
                cartoon = cv2.bitwise_and(color, color, mask=edges)

                flipped_frame[y:y + h, x:x + w] = cartoon
                #Detects eyes within the facial recognition area
                #eyes = eye_cascade.detectMultiScale(region_grey, 1.3, 5)
                #Detects smile within the facial recognition area
                #smile = smile_cascade.detectMultiScale(region_grey, 3.2, 5)

                #For the amount of eyes within the area of the facial recognition, we will draw rectangles around them
                #for (ex, ey, ew, eh) in eyes:
                    #Draws rectangles on the colored image
                    #cv2.rectangle(region_color, (ex,ey), (ex + ew , ey + eh), (0,255,0), 2)

                #for (sx, sy, sw, sh) in smile:
                    # Draws rectangles on the colored image
                    #cv2.rectangle(region_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)

    if letter == 'b':
        flipped_frame = cv2.bilateralFilter(flipped_frame, d=25, sigmaColor=750, sigmaSpace=750)
        for (x, y, w, h) in faces:
            x = x - 50
            y = y - 50
            w = w + 80
            h = h + 80
            cv2.rectangle(flipped_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # retrieves the area of the box encapsulating the recognized face
            # Y value goes first before the x value
            flipped_frame[y:y + h, x:x + w] = original[y:y + h, x:x + w]
            region_grey = gray[y:y + h, x:x + w]
            # This will ensure that we draw the rectangles around the eyes in the colored image
            region_color = flipped_frame[y:y + h, x:x + w]
            region_color_original = original[y:y + h, x:x + w]

            # We use this to smooth the image and make it cleaner while keeping the image sharp, it tells the computer
            # how many colors can be blurred together and how far the image should look for colors to blur

            # Detects eyes within the facial recognition area
            #eyes = eye_cascade.detectMultiScale(region_grey, 1.3, 5)
            # Detects smile within the facial recognition area
            #smile = smile_cascade.detectMultiScale(region_grey, 3.2, 5)

            # For the amount of eyes within the area of the facial recognition, we will draw rectangles around them
            #for (ex, ey, ew, eh) in eyes:
                # Draws rectangles on the colored image
                #cv2.rectangle(region_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            #for (sx, sy, sw, sh) in smile:
                # Draws rectangles on the colored image
                #cv2.rectangle(region_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)


    cv2.imshow('Video Feed', flipped_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):
        letter = 'a'
    elif key == ord('b'):
        letter = 'b'
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()