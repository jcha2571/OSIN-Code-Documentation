import cv2
import os
import argparse
import math
import numpy as np 

#Constants
PIXEL_AREA = 0.202 # Need to calculate
PIXEL_WIDTH = 0.449 # Need to calculate
DISTANCE_TO_CENTER = 130 # Need to measure

def guanoCalc(imageName, pathToFolder, altThreshold):
    if altThreshold:
        THRESHOLD = [(175,50,50),(200,255,255)] # Nishita
    else:
        THRESHOLD = [(0,50,50),(15,255,255)] # Normal threshold

    pathToImage = str(pathToFolder) + "/{}".format(imageName)
    image = cv2.imread(pathToImage) # Make sure forward slash or backslash is correct
    imageAngle = imageName.split("_")[-1].split(".")[0]
    imageWidth = image.shape[1]
    imageHeight = image.shape[0]
    #cv2.imshow("Original", image)

    denoised = cv2.fastNlMeansDenoisingColored(image, None, 3,3,7,21)

    image_hsv = cv2.cvtColor(denoised, cv2.COLOR_BGR2HSV) # Convert to HSV
    #cv2.imshow("HSV", image_hsv)

    threshold_hsv = cv2.inRange(image_hsv, THRESHOLD[0], THRESHOLD[1]) # Isolate brown pixels
    cv2.imshow("Threshold", threshold_hsv)

    contours, _ = cv2.findContours( threshold_hsv, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) # Generate list of contours

    # Find all contours that could be guano
    penguinColonies = []
    for cont in contours:
        if cv2.contourArea(cont) > 1000: 
            penguinColonies.append(cont)
    
    # For each colony, calculate the area, center, angle

    colonyCounter = 1
    for colony in penguinColonies:
        #Find center of colony
        M = cv2.moments(colony)
        cX = int(M["m10"]/M["m00"])
        cY = int(M["m01"]/M["m00"])
        
        # Calculate area
        area = cv2.contourArea(colony) * PIXEL_AREA

        # Calculate angle to center
        angle = int(imageAngle) + math.degrees(math.atan2(((cX - imageWidth/2)*PIXEL_WIDTH), (((imageHeight-cY)*PIXEL_WIDTH)+DISTANCE_TO_CENTER))) # Assume center of orbiter below bottom edge of image

        # Format string w/ info
        text = "Colony {colonyCounter} area: {0:.3f} mm^2\nColony {colonyCounter} location: {1:.3f} degrees".format(area, angle, colonyCounter = colonyCounter)
        print(text)

        #Number colonies in image
        image = cv2.putText(image, "{}".format(colonyCounter), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.75 , (0,0,255), 2)
        
        colonyCounter += 1

    #Save processed image
    pathToSave = str(pathToFolder) + "/PROCESSED_" + imageName
    cv2.imwrite(pathToSave, image)
    cv2.imshow("Processed Image", image)

    cv2.waitKey()
    cv2.DestroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", nargs=1, type=str, help="Name of image to process", required=True)
    parser.add_argument("-p", nargs='*', type=str, help="Path to folder where image is located", required=False, default=[os.getcwd()])
    parser.add_argument("-N", nargs='*', type=bool, help="True if image is from Nishita", required=False, default=False)
    args = parser.parse_args()
    guanoCalc(args.f[0], args.p[0], args.N)
