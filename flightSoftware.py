import os
import time
import board
import threading
import subprocess
import adafruit_fxos8700
import adafruit_fxas21002c
from shutil import copyfile
from picamera import PiCamera
from guanoDetection import hasGuano
from imuFuncs import *

i2c = board.I2C()
accelMag = adafruit_fxos8700.FXOS8700(i2c)
gyro = adafruit_fxas21002c.FXAS21002C(i2c)
camera = PiCamera(resolution=(600,600))
camera.rotation = 90

# Uncomment your address
#BDADDRESS = "DC:A6:32:33:57:2E" # Pranav
#BDADDRESS = "DC:A6:32:33:56:7D" # Nishita
#BDADDRESS = "DC:A6:32:33:57:1F" # Joseph
BDADDRESS = "DC:A6:32:55:E5:AF" # Raymond


# Global Variables
currAngle = 0
imTaken = 0
imSent = 0
bytesSent = 0
timeSending = 0
avgDataRate = 0
numOrbit = 0
targetAngle = 0
telemLock = threading.Lock()
imTakenLock  = threading.Lock()
sendLock = threading.Lock()

class takeImage(threading.Thread):
    def __init__(self, sendTelemetry, imName):
        threading.Thread.__init__(self)
        self.sendTelemetry = sendTelemetry
        self.imName = imName

    def run(self):
        global imTaken
        global imSent
        global bytesSent
        global timeSending
        global numOrbit
        global avgDataRate

        print("Starting Thread")
        print("Taking Picture")
        camera.capture("/home/pi/Pictures/allImages/%s.jpg" % self.imName)
        imTakenLock.acquire()
        imTaken += 1
        imTakenLock.release()

        # Check image for guano
        if hasGuano(self.imName):
            copyfile("/home/pi/Pictures/allImages/%s.jpg" % self.imName, "/home/pi/Pictures/guanoImages/%s.jpg" % self.imName)

            # Send file via obex"
            startTime = time.time()

            sendLock.acquire()
            sendCommand = "obexftp --bluetooth %s --channel 9 --put /home/pi/Pictures/guanoImages/%s.jpg" % (BDADDRESS, self.imName)
            subprocess.run(sendCommand, shell=True)
            sendLock.release()

            timeSending += (startTime - time.time())
            fileSize = os.path.getsize("/home/pi/Pictures/guanoImages/%s.jpg" % (self.imName))

            telemLock.acquire()
            imSent += 1
            bytesSent += fileSize
            avgDataRate = bytesSent/timeSending
            telemLock.release()

        # Check if it needs to send a telemetry packet
        if self.sendTelemetry:
            # Write telemetry packet
            packetName = "/home/pi/TelemetryPackets/Orbit%d_Packet.txt" % (numOrbit)
            packet = open(packetName, "w")
            packet.write("Number of Images Taken: %d\n" % (imTaken))
            packet.write("Number of Images Sent: %d\n" % (imSent))
            packet.write("Number of Bytes Sent: %d\n" % (bytesSent))
            packet.write("Average Data Rate: %d bytes per second" % (avgDataRate)) 
            packet.close()

            # Send telemetry packet
            sendLock.acquire()
            sendCommand = "obexftp --bluetooth %s --channel 9 --put %s" % (BDADDRESS, packetName)
            subprocess.run(sendCommand, shell=True)
            sendLock.release()

        print("Exiting Thread")

class yawTracker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global currAngle

        # Need to write code to update angle
        while True:
            currAngle = getYaw()
            time.sleep(0.01) # Update yaw every 10 milliseconds

class confirmConnection(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
            
    def run(self):
        print("Confirming connection")
        fileName = "/home/pi/TelemetryPackets/BootUpConfirm.txt" 
        currentTime = time.strftime("%H:%M:%S")
        f = open(fileName, "w")
        f.write("Confirming connection at %s" % currentTime)
        f.close()
        sendLock.acquire()
        sendCommand = "obexftp --bluetooth %s --channel 9 --put %s" % (BDADDRESS, fileName)
        subprocess.run(sendCommand, shell=True)
        sendLock.release()
        print("Connection confirmed")

def main():
    global numOrbit
    global currAngle
    global imTaken
    global targetAngle

    # Verify connection w/ ground station
    # Need to write

    time.sleep(10) # Give Pi time to boot up

    connectThread = confirmConnection()
    connectThread.start()

    # After connection confirmed, start tracking angle
    numOrbit = 0

    # Initialize angle w/ magnetometer
    currAngle = getYaw()
    print("Starting Angle: {}".format(currAngle))
    targetAngle = currAngle + 30
    targetAngle = targetAngle if targetAngle - 360 < 0 else targetAngle - 360
    print("First Target Angle: {}".format(targetAngle))
    imNumber = 1

    # Start thread for gyroscope
    yawThread = yawTracker()
    yawThread.start()

    # Main thread loop
    while True:
        # If current angle is close to targetAngle, start thread to take image
        if abs(currAngle - targetAngle) < 5:
            sendTelemetry = True if imNumber%4==0 else False
            
            imTime = time.strftime("_%H%M%S_")
            imName = str(imNumber) + str(imTime) + str(round(currAngle))

            thread = takeImage(sendTelemetry, imName)
            thread.start()

            imNumber += 1

            if sendTelemetry:
                targetAngle += 120
                numOrbit += 1
            else:
                targetAngle += 90
            
            targetAngle = targetAngle if targetAngle - 360 < 0 else targetAngle - 360

        time.sleep(0.5) # Sleep for 500 milliseconds before checking angle again
        
if __name__ == "__main__":
    main()
