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
camera = PiCamera()
bt_address = "insert here"
name = "insert here"
t = time.strftime("_%H%M%S")
imgname = ('/home/pi/%s%s.jpg' % (name,t))


def image_capture(imgname):
  time.sleep(2)
  camera.capture(imgname)
  time.sleep(2)
  return imgname

def file_t_r():
  bluetooth_turnon = "sudo hciconfig hci0 piscan"
  file_receive_command = "sudo obexpushd -B -o /bluetooth -n"
  os.system(bluetooth_turnon)
  os.system(file_receive_command)

def file_t_s():
  #IF NEEDED
  #cd_command = "cd <file_folder pathway> + /"
  bluetooth_turnon = "sudo hciconfig hci0 piscan"

  file_send_command = 'obexftp --bluetooth %s --channel 9 --put %s' % (bt_address, imgname)
  #os.system(cd_command)
  os.system(bluetooth_turnon)
  os.system(file_send_command)



image_capture(imgname)
file_t_s(imgname)




