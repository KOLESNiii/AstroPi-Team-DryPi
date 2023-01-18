from picamera import PiCamera
from time import sleep, time

camera = PiCamera()
imgCount = 0
def TakePicture(imgCount):
    camera.capture(f'image.jpg')
    imgCount += 1