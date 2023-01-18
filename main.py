try:
    from picamera import PiCamera
    cameraExists = True
except ImportError:
    print("Camera module does not work on this device.")
    cameraExists = False
from time import sleep, time

if cameraExists:
    camera = PiCamera()
imgCount = 0
def TakePicture(imgCount):
    '''Takes a picture and saves it to the current directory.'''
    if cameraExists:
        camera.capture(f'image_{imgCount}.jpg')
    imgCount += 1
    return imgCount


    
