try:
    from picamera import PiCamera
    cameraExists = True
except ImportError:
    print("Camera module does not work on this device.")
    cameraExists = False
from time import sleep, time

if cameraExists:
    camera = PiCamera()
    
TIMEBETWEENPHOTOS = 40 #seconds    

def TakePicture(imgCount):
    '''Takes a picture and saves it to the current directory.'''
    if cameraExists:
        camera.capture(f'image_{imgCount}.jpg')
    else:
        print(f'image_{imgCount}.jpg')
    imgCount += 1
    return imgCount

def getNumberString(int, targetLen = 3):
    '''Returns a string of the number with leading zeros if needed.'''
    string = str(int)
    while len(string) < targetLen:
        string = '0' + string
    return string
        
def main():
    timeVirtual = 0
    imageCount = 0
    for i in range(90*60):
        if timeVirtual % TIMEBETWEENPHOTOS == 0:
            imageCount = TakePicture(imageCount)
        timeVirtual += 1
        


    
