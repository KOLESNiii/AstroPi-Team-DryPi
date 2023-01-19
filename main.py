try:
    from picamera import PiCamera
    cameraExists = True
except ImportError:
    print("Camera module does not work on this device.")
    cameraExists = False
from time import sleep, time
from os import makedirs, path
from orbit import ISS
from pathlib import Path
    
TIMEBETWEENPHOTOS = 40 #seconds  
RUNNINGTIME = 180 #minutes-- ideally closer to 170 for actual use to be safe
TESTING = True #testing mode-- artificial environments to test certain functions
PROGRAMPATH = Path(__file__).parent.resolve() #path to this file

def MakeDirs():
    '''Makes the folders for images and other save files.'''
    makedirs(f'{PROGRAMPATH}/images/', exist_ok = True)
    
def ConvertCoordinates(angle):
    '''
    Converts a 'skyfield' angle to a string of degrees, minutes, and seconds.
    
    Returns a string of the converted angle.
    '''        
    sign, degrees, minutes, seconds = angle.signed_dms()
    coordinate = degrees + minutes/60 + seconds/3600
    coordinate *= sign
    return str(coordinate)

def TakePicture(camera, imgCount):
    '''Takes a picture and saves it to the current directory.'''
    
    currentLocation = ISS.coordinates()
    latitude = ConvertCoordinates(currentLocation.latitude)
    longitude = ConvertCoordinates(currentLocation.longitude)
    #TODO:
    #add this to CSV file along with timestamp
    if cameraExists:
        camera.exif_tags['GPS.GPSLatitude'] = latitude #cannot store signed numbers in these fields
        camera.exif_tags['GPS.GPSLongitude'] = longitude
        camera.exif_tags['GPS.GPSLatitudeRef'] = 'S' if currentLocation.latitude.degrees < 0 else 'N' #if negative, is S
        camera.exif_tags['GPS.GPSLongitudeRef'] = 'W' if currentLocation.longitude.degrees < 0 else 'E' #if negative, is W
        camera.capture(f'{PROGRAMPATH}/images/image_{imgCount}.jpg')
        sleep(2) #camera processing time
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

def Finish(camera):
    '''Closes the camera and ends the program.'''
    if cameraExists:
        camera.close()
    exit()
        
def main():
    if cameraExists:
        camera = PiCamera()
        camera.resolution = (4056, 3040)
        sleep(1) #camera warmup
    elif not TESTING: #If the camera module does not work and we are not testing locally
        raise ImportError("Camera module could not be imported. Exiting.")
    else:
        camera = None
    
    MakeDirs()
    imageCount = 0
    
    if TESTING:
        timeVirtual = 0
        while timeVirtual < RUNNINGTIME*60: #90 virtual minutes
            if timeVirtual % TIMEBETWEENPHOTOS == 0:
                imageCount = TakePicture(camera, imageCount)
            timeVirtual += 1
    else:
        lastTime = time()
        startTime = time()
        while time() - startTime <= RUNNINGTIME*60: #90 minutes
            if time() - lastTime >= TIMEBETWEENPHOTOS:
                imageCount = TakePicture(camera, imageCount)
                lastTime = time()
        
    Finish(camera)
    
main()
        


    
