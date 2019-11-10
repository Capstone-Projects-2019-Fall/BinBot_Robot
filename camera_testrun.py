import picamera

print("About to take a picture")
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.capture("/home/pi/Desktop/newImage.jpg")
print("Picture was taken with pi camera")