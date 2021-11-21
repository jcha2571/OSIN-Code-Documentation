import os
import time
import board
import math
import busio
import adafruit_fxos8700
from git import Repo
from picamera import PiCamera

#SETUP IMU AND CAMERA
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)
camera = PiCamera(resolution=(600,600))

def image_capture():
  #time.sleep(2)
  starttime = time.time()
  #camera_cap = "raspistill -o test.jpg"
  #camera.capture(test)
  #os.system(camera_cap)
  camera.capture("/home/pi/Julius-Freezer/Images/Pranav/speedTest.jpg")
  endtime = time.time()
  print("Image captured in %s seconds" % (endtime-starttime))
  #time.sleep(2)
  
def file_t_r():
  bluetooth_turnon = "sudo hciconfig hci0 piscan"
  file_receive_command = "sudo obexpushd -B -o /bluetooth -n"
  os.system(bluetooth_turnon)
  os.system(file_receive_command)
  
def file_t_s():
  time.sleep(10)
  starttime = time.time()
  #IF NEEDED
  #cd_command = "cd <file_folder pathway> + /"
  bluetooth_turnon = "sudo hciconfig hci0 piscan"
  
  file_send_command = "obexftp --bluetooth DC:A6:32:33:57:2E --channel 9 --put home/pi/Julius-Freezer/Images/Pranav/speedTest.jpg"
  #os.system(cd_command)
  os.system(bluetooth_turnon)
  os.system(file_send_command)
  endtime = time.time()
  print("File sent in : %s seconds" % (endtime - starttime))


def makeTelemetryPacket():
  starttime = time.time()
  f = open("/home/pi/Julius-Freezer/Images/Pranav/sampleTelemetry.txt", "w")
  f.write("Images Taken: 3, Images Sent: 2, Average Data Rate: 2 kB/s, kB sent: 500")
  f.close()
  endtime = time.time()
  print("Time to write: %s seconds" % (endtime - starttime))

def git_push_gs():
  starttime = time.time()
  try:
    repo = Repo('/home/pi/Julius-Freezer')
    repo.git.add('/home/pi/Julius-Freezer/Images/Pranav/speedTest.jpg')
    repo.git.add('/home/pi/Julius-Freezer/Images/Pranav/sampleTelemetry.txt')
    repo.index.commit('New Photo')
    print('made the commit')
    origin = repo.remote('origin')
    print('added remote')
    origin.push()
    print('pushed changes')
  except:
    print('Couldn\'t upload to git')
  endtime = time.time()
  print("Pushed to Git in: %s seconds" % (endtime - starttime))

starttime = time.time()
image_capture()
makeTelemetryPacket()
#file_t_s()
git_push_gs()
endtime = time.time()
print("Total time seconds: %s seconds" % (endtime -starttime))
