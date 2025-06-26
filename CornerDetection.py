import numpy as np
import cv2

img = cv2.imread('static/chessboard2.png')
img= cv2.resize(img,(0,0), fx=2.5, fy=2.5)

#Changes our image to black and white
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#This will be used to detect the corners of an image
#
corners = cv2.goodFeaturesToTrack(gray, 100,0.01, 10)
print(corners)
corners = np.int8(corners)

for corner in corners:
    #ravel helps to flatten the array
    x,y = corner.ravel()
    cv2.circle(img,(x,y), 5, (255,0,0), 3)


cv2.imshow("frame", img)
cv2.waitKey(0)
cv2.destroyAllWindows()