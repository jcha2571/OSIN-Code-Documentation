import board
import math
import time
import adafruit_fxos8700
import adafruit_fxas21002c

i2c = board.I2C()
accelMag = adafruit_fxos8700.FXOS8700(i2c)
gyro = adafruit_fxas21002c.FXAS21002C(i2c)

#Uncomment your offsets
#magOffsets = [-31.15, -60.00, -51.65] # Pranav
#magOffsets = [-33.05, -51.75, -57.9] # Joseph
#magOffsets = [-19.6, -69.7, -68.6] # Nishita
magOffsets = [-6.850,-40.700,-48.300] # Raymond

def magCalibration():
    print("Starting calibration in 5 seconds")
    print("Rotate magnetometer around all 3 axes until the offsets stop changing")
    print("Press any ctrl-c to end calibration")
    
    time.sleep(5)
    print("Starting Calibration")
    magX, magY, magZ = accelMag.magnetometer

    minX = magX
    minY = magY
    minZ = magZ
    
    maxX = magX
    maxY = magY
    maxZ = magZ

    while True:
        magX, magY, magZ = accelMag.magnetometer

        # Find min values
        minX = min(minX, magX)
        minY = min(minY, magY)
        minZ = min(minZ, magZ)

        # Find max values
        maxX = max(maxX, magX)
        maxY = max(maxY, magY)
        maxZ = max(maxZ, magZ)

        # Calculate offset values (avg of min and max)
        offsetX = (minX + maxX)/2
        offsetY = (minY + maxY)/2
        offsetZ = (minZ + maxZ)/2

        print("Offset Values (x,y,z): ({0:.3f},{1:.3f},{2:.3f})".format(offsetX,offsetY,offsetZ))
        
        time.sleep(0.01)

def getRoll():
    accelX, accelY, accelZ = accelMag.accelerometer
    accelY = -accelY
    accelZ = -accelZ
    return math.degrees(math.atan2(accelY, math.sqrt(accelX**2 + accelZ**2)))

def getPitch():
    accelX, accelY, accelZ = accelMag.accelerometer
    accelY = -accelY
    accelZ = -accelZ
    return math.degrees(math.atan2(accelX, math.sqrt(accelY**2 + accelZ**2)))

def getYaw():
    magX, magY, magZ = accelMag.magnetometer
        
    magX = magX - magOffsets[0]
    magY = magY - magOffsets[1]
    magZ = magZ - magOffsets[2]
    
    magY = -magY
    magZ = -magZ

    roll = math.radians(getRoll())
    pitch = math.radians(getPitch())

    Xh = magX * math.cos(pitch) + magY * math.sin(roll) * math.sin(pitch) + magZ * math.cos(roll) * math.sin(pitch)
    Yh = magY * math.cos(roll) + magZ * math.sin(roll)

    heading = 180-math.degrees(math.atan2(-Yh, Xh))

    return heading

if __name__ == "__main__":
    magCalibration()
   # while True:
        #print("Pitch: {0:.2f}".format(getPitch()))
        #print("Roll: {0:.2f}".format(getRoll()))
    #    print("Yaw: {0:.2f}".format(getYaw()))
     #   time.sleep(1)
