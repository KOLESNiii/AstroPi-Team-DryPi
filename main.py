try:
    from picamera import PiCamera
    cameraExists = True
except ImportError:
    print("Camera module does not work on this device.")
    cameraExists = False
from time import sleep, time
from os import makedirs, path

if cameraExists:
    camera = PiCamera()
    camera.resolution = (4056, 3040)
    
TIMEBETWEENPHOTOS = 40 #seconds  
RUNNINGTIME = 180 #minutes-- ideally closer to 170 for actual use to be safe
TESTING = True #testing mode-- artificial environments to test certain functions

def MakeDirs():
    '''Makes the folders for images and other save files.'''
    makedirs('./images/', exist_ok = True)
    

def TakePicture(imgCount):
    '''Takes a picture and saves it to the current directory.'''
    if cameraExists:
        camera.capture(f'./images/image_{imgCount}.jpg')
        sleep(2)
    else:
        print(f'image_{imgCount}.jpg')
    imgCount += 1
    return imgCount

def GetNumberString(int, targetLen = 3):
    '''Returns a string of the number with leading zeros if needed.'''
    string = str(int)
    while len(string) < targetLen:
        string = '0' + string
    return string

def Finish():
    '''Closes the camera and ends the program.'''
    if cameraExists:
        camera.close()
    exit()
        
def main():
    if not TESTING and not cameraExists: #If the camera module does not work and we are not testing locally
        raise ImportError("Camera module could not be imported. Exiting.")
    
    MakeDirs()
    imageCount = 0
    
    if TESTING:
        timeVirtual = 0
        while timeVirtual < RUNNINGTIME*60: #90 virtual minutes
            if timeVirtual % TIMEBETWEENPHOTOS == 0:
                imageCount = TakePicture(imageCount)
            timeVirtual += 1
    else:
        lastTime = time()
        startTime = time()
        while time() - startTime <= RUNNINGTIME*60: #90 minutes
            if time() - lastTime >= TIMEBETWEENPHOTOS:
                imageCount = TakePicture(imageCount)
                lastTime = time()
        
    Finish()
    
main()
        


    
