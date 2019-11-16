# Author: Jose Silva
# Date Created: November 9th, 2019
# File Name: Camera.py
# Description: Camera functionality

from __future__ import division

import base64
import picamera
import picamera.array
import cv2
import time


# Setting up Raspberry Pi camera
# camera = PiCamera() # Raspberry Pi Camera
# camera.resolution = (640, 480)
# camera.framerate = 20


def init_camera():
    camera = picamera.PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 30
    return camera


def take_photo():
    camera = picamera.PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(5)
    print("About to take a photo")
    camera.capture("/home/pi/Desktop/newImage.jpg")
    print("Finished taking a photo")
    camera.stop_preview()


def capture_img_stream(camera):
    with camera:
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            # At this point the image is available as stream.array
            image = stream.array

            encoded, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            print("jpg as text: %s", jpg_as_text)
            return image


if __name__ == '__main__':

    from src.interfaces.Connection import Connection
    from src.instructions.instruction import Instruction
    from src.interfaces import Camera

    Jose_laptop = "192.168.43.116"
    SeanR_laptop = "192.168.43.156"
    SeanD_laptop = "192.168.43.68"

    IP = SeanR_laptop
    PORT = 7001

    camera = Camera.init_camera()
    try:
        # take_photo()
        # cv2.imshow("Image", capture_img_stream())
        # cv2.waitKey(0)
        img = Camera.capture_img_stream(camera)

        instr_out = Instruction(Instruction.FROM_DATA, "PATROL", img, None, None)

        connection = Connection(IP, PORT)
        connection.send(instr_out.json())
        msg_in = connection.receive()
        connection.close()
    except Exception as e:
        print("take_photo exception: %s", e)



