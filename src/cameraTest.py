
from picamera import PiCamera
from time import sleep


class CameraTest:

    # Test to take a photo using Raspberry camera and save it to desktop
    def take_photo_test(self):
        camera = PiCamera()
        camera.start_preview()
        sleep(5)
        camera.capture('C:\Users\Silva_Surfer\Pictures')
        camera.stop_preview()

    take_photo_test()


