# Global vars
#Used to signify of all the required imports were successfully imported
validImports = None
#Used to validate if the camera object was successfully initialized
cameraInitialized = None
#Validates if the camera feed has successfully started and is up and running
cameraCaptureStarted = None


#if __name__ == '__main__':

# Make sure all required files are imported
try:
    import datetime
    from motionCapture import MotionCapture
    from Marker import Marker

    '''
    import disableLightRing
    import enableLightRing
    import RPi.GPIO as GPIO
    '''




#We make sure to make the validImports false if there is a module not found error
except ModuleNotFoundError as e:
    print(e)
    validImports = False
else:
    validImports = True

# If all modules were imported, attempt to start camera
if validImports:
    print("Initializing camera...")

    # Attempt to initialize the camera object
    try:
        vid = MotionCapture()
    except:
        print("Could not initialize camera")
        cameraInitialized = False
    else:
        cameraInitialized = True

    # If the camera was successfully initialized, attempt to start the capture feed
    if cameraInitialized:
        print("Camera initialized")

        print("Attempting to start camera capture feed...")
        try:
            vid.startCapture()
        except:
            print("Could not start camera capture feed")
            cameraCaptureStarted = False
    else:
        cameraCaptureStarted = False


# Otherwise, don't bother starting up camera
else:
    print("Could not load modules. Aborting camera operation")

# Marker testing
'''
markerList = []
marker1 = Marker(123, 321, "A", "1")
marker1.printCoords()

for i in range (1, 10):
    markerList.append(Marker(111, 222, "A", i))


marker1.printTimeStamp()

marker2 = Marker(123, 333, "A", "2")
marker2.printTimeStamp()


for marker in markerList:
    marker.printTimeStamp()
'''

