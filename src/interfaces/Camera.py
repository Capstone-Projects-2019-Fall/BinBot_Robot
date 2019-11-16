# Author: Jose Silva
# Date Created: November 9th, 2019
# File Name: Camera.py
# Description: Camera functionality

from __future__ import division
import picamera
import time


# Setting up Raspberry Pi camera
# camera = PiCamera() # Raspberry Pi Camera
# camera.resolution = (640, 480)
# camera.framerate = 20
class Camera:

    def take_photo(self):
        camera = picamera.PiCamera()
        camera.resolution = (1280, 720)
        camera.framerate = 30
        camera.start_preview()
        time.sleep(5)
        print("About to take a photo")
        camera.capture("/home/pi/Desktop/newImage.jpg")
        print("Finished taking a photo")
        camera.stop_preview()


if __name__ == '__main__':
    try:

        take_photo()

    except Exception as e:
        print("take_photo exception: %s", e)



