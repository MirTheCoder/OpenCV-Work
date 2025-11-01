#This library will be used to handle camera inputs
#and image processing as well
import cv2
import numpy as np
import datetime
import os.path
import fake_rpi
import sys

import sys
#This will act like the raspberry pi hardware modules required for the RPi.GPIO
import fake_rpi
from Marker import Marker

#This will set the RPI and RPI.GPIO to the fake_rpi values so that when the system checks
#for them before downloading RPi.GPIO, it will pass the test
sys.modules['RPi'] = fake_rpi.RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO

#The RPI.GPIO, controls Raspberry Pi GPIO
#pins to turn the infrared light on and off
import RPi.GPIO as GPIO

'''
Class for MotionCapture object. Bulk of the magic is done here, utilizing the openCV library for tracking and displaying.
This class contains functions to convert images to grayscale, utilize the openCV library for tracking whitespace and 
displaying them as markers, denoting with a green box the coordinates.

'''


class MotionCapture:

    # Default constructor. No parameters needed
    #This is the framework we will be using to create an instance for our motion capture video
    def __init__(self):
        self.showVideo = True #This will determine if we ought to show the live video feed
        self.showFPS = True #This will determine if we show the frame rate on the screen or not
        self.showMarkers = True #This will determine if we will or will not draw boxes around the identified markers
        self.showCoordinates = True #Whether we show the coordinates
        self.showMarkerCount = True #Whether we show the number of markers or not
        self.markerCount = 0
        self.markerList = [] #Where we will store all the objects in the detected frame
        #This will hold the markers from the previous list in order for us to compare and keep
        #track of moving blobs
        self.oldMarkerList = []

        # Set default color to Green
        self.markerColor = (0, 255, 0)
        self.thresholdValue = 30  # High default threshold value to ensure that white markers are precisely denoted
        self.maxThresholdValue = 255

        self.fpsCounter = 0
        #We are going to use this to compare each frame to the previous frame to see if there
        #has been any change in order to detect motion
        self.previousFrame = None
        self.startTime = None
        self.currentFPS = 0
        self.GPIOPin = 7  # Enable Pin for Light Ring
        GPIO.setwarnings(False)  # Disable Warnings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.GPIOPin, GPIO.OUT)

    '''
    This method will display the frames per second being captured by the camera in the upper left hand corner
    @params image -> What image frame to display the text to
    '''
    #Used to display our frame rate on the screen
    def displayFPS(self, image):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, "FPS: {0}".format(self.currentFPS),
                    (25, 25), font, .75, (255, 255, 0), 2)

    '''
    This method is a blanket method to draw text in a passed in location, given the parameters
    @params image     -> The image frame to display text to
            text      -> The text string to display
            location  -> X, Y coordinate to display the text
            fontSize -> Size of the text's font
            color     -> Color of the text
            thickness -> Thickness of the font
    '''

    def drawText(self, image, text, location, fontSize, color, thickness):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, location, font, fontSize, color, thickness)

    '''
    This method takes in an image still and converts it to grayscale
    @params image -> The image to turn into grayscale
    @return The converted image to grayscale

    '''
    #Converts the image color to a gray scale image
    def getGrayScale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # make image gray scale

    '''
    This method will determine if the input grayscale image is within the whitespace threshold. 
    Utilize THRESH_BINARY to convert all pixels to either 0 for white, or 1 for black.
    @params gray_image -> The grayscale image to process
    @return The threshold image after determining the threshold rating for the image

    '''
    #Will return a binary image that contains pixels with brightness level at the threshold level that has been stated
    def getThresholdMask(self, grayScaleImage):
        th, dst = cv2.threshold(grayScaleImage, self.thresholdValue, self.maxThresholdValue,
                                cv2.THRESH_BINARY)  # apply filter
        return dst

    '''
    This method will write the input image still to hard disk with a unique name, as to not overwrite files.
    @params image -> The image still to write to hard disk

    '''
    #used to save current camera frame as a jpeg image
    #This is how we keep track of all the frames that we get to ensure that we can count the amount
    #of frames per second
    def writeMethod(self, image):
        counter = 1
        while os.path.isfile("image{0}.jpg".format(counter)):
            counter += 1
        cv2.imwrite("image{0}.jpg".format(counter), image)

    '''
    This method enables the IR Light Ring for the camera
    '''

    def enableLightRing(self):
        GPIO.output(self.GPIOPin, GPIO.HIGH)

    '''
    This method disables the IR Light Ring for the camera
    '''

    def disableLightRing(self):
        GPIO.output(self.GPIOPin, GPIO.LOW)

    '''
    This method is a blanket method to toggle a boolean value, i.e. a camera setting that is either True or False
    @params option -> The bool value to toggle

    '''

    def toggle(self, option):
        if option is False:
            return True
        if option is True:
            return False

    '''
    This method will locate and process markers on a given image. 
    The processing of markers involves finding them via whitespace, granted by the grayscale thresholding, and 
    bounding a box around them. 
    This will refresh every frame the camera captures. Storing and creation of the markers is also processed here
    @params image -> The image still (frame) to locate markers

    '''

    def findMarkers(self, image):
        try:
            sameMarker = False
            grayScaleImage = self.getGrayScale(image)
            #We will blur the image a little in order to prevent the camera from picking up
            #subtle light flickering as motion
            grayScaleImage = cv2.GaussianBlur(grayScaleImage, (21, 21), 0)
            frameDelta = grayScaleImage
            #Checking to see if there is an array in the previous frame (If it has a frame loaded
            #in it already)
            if not isinstance(self.previousFrame, np.ndarray):
                #We will make sure to store the initial frame within our previous frame placeholder
                self.previousFrame = grayScaleImage
            else:
                #Used to get an array of difference in pixel value from previous frame to current
                #frame
                frameDelta = cv2.absdiff(self.previousFrame, grayScaleImage)
            #For the first frame, we will pass just the grayScaleImage, and then everything else will
            #be based off the differences in motion

            binaryThresholdImage = self.getThresholdMask(frameDelta)
            #This will allow us to join whitespaces together so that we don't get fragmented boxes
            #for things like a hand or something (allows to make a bigger box to contain moving
            #obejcts)

            #we are practically just spreading the white pixels or expanding them across the frame
            #in order to get a bigger contour result
            binaryThresholdImage = cv2.dilate(binaryThresholdImage, None, iterations=1.5)
        except Exception as e:
            print(f"Error while dilating difference in frame: {e}")

        # Make copy, since findContours() is destructive (it edits the original image you pass into it)

        #This will give us an outline of the white markers by providing us with the x,y coordinates that
        #make up the edge of each image

        #We use the cv2.RETR_EXTERNAL because it retrieves the outermost outlines of the white markers, which
        #helps to ensure that we don't retrieve an outline within an outline

        #We use cv2.CHAIN_APPROX_SIMPLE to ensure that we only return necessary points, so if a straight
        #or consisted line holds multiple points, we would just return the end points of that line, since all the points
        #lie perfectly between these two points
        #In opencv 4.0 and above, the cv2.findContours returns only two separate values instead of three
        contourList, hierarchy = cv2.findContours(binaryThresholdImage.copy(), cv2.RETR_EXTERNAL,
                                                             cv2.CHAIN_APPROX_SIMPLE)

        if len(contourList) > 0:  # check if at least 1 marker was found
            tempCount = 0

            # Start of fresh frame, reset timestamp and number of markers
            i = len(contourList)
            timestamp = datetime.datetime.now()

            execLocation = "(DrawingContourListBoxes)"
            for contour in contourList:
                #We will only keep the contour values that are of the size of interest for us
                #we don't want contour values for small and trivial things
                if cv2.contourArea(contour) > 750:
                    try:
                        #We want only 20 markers at a time
                        if tempCount < 20:
                            tempCount += 1
                            #Returns to us the smallest possible rect that can contain a contour or outline
                            #of a marker
                            rect = cv2.minAreaRect(contour)
                            #Used to turn the minAreaRect values into actual 4 corner values for the rectangle
                            box = cv2.boxPoints(rect)
                            #box = np.int0(box) is the old way of doing this as the new versions (version 1.24 and above)
                            #no longer support this alias and instead used the raw one down below
                            box = box.astype(np.int32)
                            if tempCount != 1:
                                if len(self.oldMarkerList) > 0:
                                    for val in self.oldMarkerList:
                                        #We use .all() to see if each value is identical within the arrays
                                        if (val == box).all():
                                            print("Motion detected")
                                            sameMarker = True
                                        else:
                                            sameMarker = False

                            #box = box.astype(np.intp)

                            #We will only draw a the marker if it is new and not an old one
                            if not sameMarker:
                                cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
                                x, y, x2, y2 = cv2.boundingRect(contour)
                                centerX = int(x + (x2 / 2))
                                centerY = int(y + (y2 / 2))

                                # Draw an identifying label on top of each marker
                                self.drawText(image, "A" + str(len(contourList) - i), (centerX, centerY - 25), .50, (0, 255, 255),
                                              1)

                                # Draw a circle denoting centerpoint of marker
                                cv2.circle(image, (centerX, centerY), 2, (0, 0, 255), -1)

                            try:

                                if (len(self.markerList) == 0):
                                    print("Creating first marker")
                                elif (len(self.markerList) < len(contourList)):
                                    print("Creating new marker")
                                else:
                                    pass
                                if not sameMarker:
                                    temp = Marker(centerX, centerY, "A", len(contourList) - i, timestamp)
                                    self.markerList.append(temp)

                                    self.oldMarkerList.append(box)
                                    # This makes sure that our list stays at a length of no more than 20
                                    if len(self.oldMarkerList) >= 20:
                                        self.oldMarkerList.pop(0)
                                    temp.printTest()

                                i = i - 1
                            except:
                                print("Error creating marker object or appending")
                        else:
                            if len(self.markerList) > 0:
                                self.markerList.pop(0)
                    except Exception as e:
                        print(f"Error at: {execLocation} - Error: {e}")

        else:
            del self.markerList[:]

    '''
    This method will control the starting and stopping of video capture from the camera, activation of other class functions, 
    and keypresses while video frame is active and in focus. 

    '''

    def startCapture(self):
        try:
            # We will delete the markers from the previous capture in order to start fresh for this new camera feed
            del self.markerList[:]
            #Where we start the video capture on an infinite loop till it is stopped manually. The zero
            #tells the computer to use the default camera
            cap = cv2.VideoCapture(0)
            #Used to set the frame rate to 120 frames per second, opencv will select the closest
            #frame rate to use if yur camera can't support 120 frames per second
            cap.set(cv2.CAP_PROP_FPS, 120)
            #This will set the pixel size of each frame
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
            #Used to get the fps (frames per second) of the camera
            fps = cap.get(cv2.CAP_PROP_FPS)
        except:
            print("Ran into an issue starting camera feed")
        else:
            print("Camera capture started successfully")
        # Set Time
        self.startTime = datetime.datetime.now()
        while True:

            self.fpsCounter += 1
            ret, frame = cap.read()
            # frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5) # Deprecated by above line
            self.currentFPS = int(self.fpsCounter / (datetime.datetime.now() - self.startTime).total_seconds())
            if self.showMarkers:
                self.findMarkers(frame)
            if self.showFPS:
                self.drawText(frame, str(fps), (int(frame.shape[:2][1] * .9), 20), 0.75, (0, 0, 255), 2)
                self.displayFPS(frame)
            if self.showVideo:
                #Used to flip the frame so that it mirrors your actions
                cv2.imshow("Video", frame)

            '''
				Keypress events
	    '''
            keyPress = cv2.waitKey(1) & 0xFF
            # Close down the video frame, stop capturing, and disable lightring
            if keyPress == ord('q'):
                self.disableLightRing()
                cap.release()
                break

            # Write a still image from the camera to drive
            if keyPress == ord('s'):
                self.writeMethod(frame)

            # Display the current frames/sec on the video frame
            if keyPress == ord('f'):
                self.showFPS = self.toggle(self.showFPS)

            # Display markers in view on the video frame
            if keyPress == ord('m'):
                self.showMarkers = self.toggle(self.showMarkers)
                print("Show markers set to {0}".format(self.showMarkers))

            # Enable the light ring for the camera (on e key pressed)
            if keyPress == ord('e'):
                self.enableLightRing()
            # Disable the lightring for the camera (on d key pressed)
            if keyPress == ord('d'):
                self.disableLightRing()

            # Decrease the threshold of whitelight capture (On Up Arrow Pressed)
            if keyPress == 84:
                self.thresholdValue = self.thresholdValue - 1
                print("Decreasing threshold to {0}".format(self.thresholdValue))

            # Increase the threshold of whitelight capture (On Down Arrow Pressed)
            if keyPress == 82:
                self.thresholdValue = self.thresholdValue + 1
                print("Increasing threshold to {0}".format(self.thresholdValue))
