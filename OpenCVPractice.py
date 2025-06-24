import cv2
import random
#Used to load images into the file, put how you want to load the image next to the images path as shown below
img = cv2.imread('static/gummy.jpg', 1)
#Used to resize the size of the image, the fx and fy changes the height and width by multiplying the original picture
#Dimensions by the values you pass into it
figure = cv2.resize(img,(0,0), fx=2, fy=2)
# -1 or cv2.IMREAD_COLOR: loads a color image and ignores any transparency of the image
# 0 or cv2.IMREAD_GRAYSCALE: loads images in black and white
# 1 or cvs.IMREAD_UNCHANGED: loads the image as is

#This will rotate the image
rotate = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

#img = cv2.imwrite() is used to save your image to the file destination that you set

#This is how we are going to show this image, it will open a window and display the image with the title we entered
cv2.imshow('Image',img)

#This controls how long the window will be open for, the zero makes the window stay open infinitely until you press
#a key
cv2.waitKey(0)

cv2.imshow('Image',figure)
cv2.waitKey(0)

cv2.imshow('Image',rotate)
cv2.waitKey(0)

#This will close all of our windows
cv2.destroyAllWindows()


#img.shape() will give you the (rows, columns, channels)

#This will be used to change the pixels to random colors
num = img.shape[0]
print(num)
val = img.shape[1]
print(val)
num = (int)(num/7)
print(num)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if j <= num:
            #Chooses a random int value to pass into the pixels parameters, a value between 0 and 255
            img[i][j] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        elif num <= j and j <= (num*2):
            img[i][j] = img[i][j]
        elif num*2 <= j and j <= (num * 3):
            img[i][j] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        elif num*3 <= j and j <= (num*4):
            img[i][j] = img[i][j]
        elif num*4 <= j and j <= (num * 5):
            img[i][j] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        elif num*5 <= j and j <= (num * 6):
            img[i][j] = img[i][j]
        else:
            img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#260 by 194


img = cv2.imread('static/gummy.jpg', 1)
#This is used to capture pieces of an image based off row and column coordinates
tag = img[150:240, 150:190]
#We will replace the image location with what we stored in tag
img[50:140, 50:90] = tag
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()