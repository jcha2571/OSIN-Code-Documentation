import cv2
import time
import numpy as np

THRESHOLD = [(0,50,50),(15,255,255)] # Normal
#THRESHOLD = [(175,50,50),(200,255,255)] # Nishita

def hasGuano(imgName):
    pathToImage = "/home/pi/Pictures/allImages/%s.jpg" % imgName
    #pathToImage = "C:\\Users\\Pranav Budhia\\Downloads\\%s.jpg" % imgName
    image = cv2.imread(pathToImage) 
    #cv2.imshow("Original", image)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # Convert to HSV

    threshold_hsv = cv2.inRange(image_hsv, THRESHOLD[0], THRESHOLD[1]) # Isolate brown pixels

    #cv2.imshow("Mask", threshold_hsv)
    #print(cv2.countNonZero(threshold_hsv))

    #cv2.waitKey()
    #cv2.DestroyAllWindows()

    if cv2.countNonZero(threshold_hsv) > 1500:
        return True

    return False
