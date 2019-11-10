# Author: Jose Silva
# Date Created: November 9th, 2019
# File Name: Camera.py
# Description: Camera functionality

from __future__ import division
import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685 # Library that helps control servos

from picamera import PiCamera
from time import sleep

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# Setting up Raspberry Pi camera
camera = PiCamera() # Raspberry Pi Camera
camera.resolution = (640, 480)
#camera.framerate = 20

class Camera:


    def take_photo(self):
        camera = PiCamera()
        camera.start_preview()
        sleep(5)
        camera.capture("/home/pi/Desktop/newImage.jpg")
        camera.stop_preview()







'''
def camera_ang(direction, ang):  # Camera angle method
    global org_pos
    if ang == 0:
        ang = 4
    if direction == 'lookdown':
        if org_pos <= L11_MAX:
            org_pos += ang
        else:
            org_pos = L11_MAX
    elif direction == 'lookup':
        if org_pos >= L11_MIN:
            org_pos -= ang
        else:
            org_pos = L11_MIN
    elif direction == 'home':
        org_pos = L11_MAX
    else:
        pass
    # print(ang)
    pwm.set_pwm(11, 0, org_pos)
'''