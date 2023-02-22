from time import sleep, time, strftime, gmtime
from os import makedirs, path
from orbit import ISS
from pathlib import Path
import logging, csv

    
TIMEBETWEENPHOTOS = 30 #seconds  
TIMEBETWEENDATALOGS = 10 #seconds
RUNNINGTIME = 178 #minutes-- ideally closer to 170 for actual use to be safe
TESTING = True #testing mode-- artificial environments to test certain functions
VIRTUALTIMEGAP = 1   #second gap between each virtual "second" in testing mode
PROGRAMPATH = Path(__file__).parent.resolve() #path to this file
logging.basicConfig(filename=f'{PROGRAMPATH}/all.log', level=logging.DEBUG, filemode="w",format='%(asctime)s %(message)s')

try:
    from picamera import PiCamera
    cameraExists = True
except ImportError:
    logging.warning("Camera module could not be imported on this device.")
    cameraExists = False

def addCSVEntry(imageTaken = False, imgNum = None):
    '''Adds a row to the CSV file with the given data.'''
    latitude, longitude, _ = getLocation()
    latitude, longitude = float(latitude), float(longitude)
    time = strftime("%H:%M:%S", gmtime())

    with open(f'{PROGRAMPATH}/data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([imageTaken, imgNum, latitude, longitude, time])


def MakeDirs():
    '''Makes the folders for images and other save files.'''
    makedirs(f'{PROGRAMPATH}/images/', exist_ok = True)
    with open(f'{PROGRAMPATH}/data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image Taken', 'Image Number', 'Latitude', 'Longitude', 'Time'])
    logging.info("Created directories for images and other save files.")
    
def ConvertCoordinates(angle):
    '''
    Converts a 'skyfield' angle to a string of degrees, minutes, and seconds.
    
    Returns a string of the converted angle.
    '''        
    sign, degrees, minutes, seconds = angle.signed_dms()
    coordinate = degrees + minutes/60 + seconds/3600
    coordinate *= sign
    return str(coordinate)

def getLocation(advanced = False):
    '''Returns the current location of the ISS as a tuple of (latitude, longitude, (latitude sign, longitude sign)).'''
    currentLocation = ISS.coordinates()
    latitude = ConvertCoordinates(currentLocation.latitude)
    longitude = ConvertCoordinates(currentLocation.longitude)
    if advanced:
        angles = (currentLocation.latitude.degrees, currentLocation.longitude.degrees)
    else:
        angles = None
    return (latitude, longitude, angles)

def TakePicture(camera, imgCount):
    '''Takes a picture and saves it to the current directory.'''
    
    latitude, longitude, angles = getLocation(True)
    latAngle, longAngle = angles

    if cameraExists:
        camera.exif_tags['GPS.GPSLatitude'] = latitude #cannot store signed numbers in these fields
        camera.exif_tags['GPS.GPSLongitude'] = longitude
        camera.exif_tags['GPS.GPSLatitudeRef'] = 'S' if latAngle < 0 else 'N' #if negative, is S
        camera.exif_tags['GPS.GPSLongitudeRef'] = 'W' if longAngle < 0 else 'E' #if negative, is W
        camera.capture(f'{PROGRAMPATH}/images/image_{imgCount}.jpg')
        sleep(2) #camera processing time
    imgCount += 1
    logging.info("Taken picture " + str(imgCount))
    return imgCount

def GetNumberString(int, targetLen = 3):
    '''Returns a string of the number with leading zeros if needed.'''
    string = str(int)
    while len(string) < targetLen:
        string = '0' + string
    return string

def Finish(camera):
    '''Closes the camera and ends the program.'''
    logging.warning("Program ended cleanly.")
    if cameraExists:
        camera.close()
    exit()
        
def main():
    if cameraExists:
        camera = PiCamera()

        allowed = False 
        resolutions = [(4056, 3040), (3840, 2160), (3072, 2048), (2592, 1944), (1920, 1080), (1640, 1232), (1296, 972), (640, 480)]
        next_try = 0
        while not allowed: #try to set the camera resolution to the highest possible, as we encountered out of memory errors when testing on high resolutions
            try:
                camera.resolution = resolutions[next_try]
            except:
                next_try += 1
                continue
            allowed = True

        sleep(1) #camera warmup
        logging.info("Camera initialised.")

    elif not TESTING: #If the camera module does not work and we are not testing locally
        logging.critical("Camera module could not be imported. Exiting.")
        raise ImportError("Camera module could not be imported. Exiting.")
    else:
        camera = None
        logging.warning("Camera module could not be imported. Continuing in testing mode.")
    
    MakeDirs()
    imageCount = 0
    
    if TESTING:
        logging.info("Running in testing mode.")
        logging.warning("Will run for " + str(RUNNINGTIME*VIRTUALTIMEGAP) + " minutes.")
        logging.warning("Process should terminate at " + strftime("%H:%M:%S", gmtime(time() + RUNNINGTIME*VIRTUALTIMEGAP*60)) + ".")
        timeVirtual = 0
        while timeVirtual < RUNNINGTIME*60: #180 virtual minutes
            if timeVirtual % TIMEBETWEENPHOTOS == 0:  
                imageCount = TakePicture(camera, imageCount)
                addCSVEntry(True, imageCount)
            if timeVirtual % TIMEBETWEENDATALOGS == 0:
                addCSVEntry(imgNum=imageCount)
            timeVirtual += 1
            sleep(VIRTUALTIMEGAP)
    else:
        lastImageTime = time()
        lastDataLogTime = time()
        startTime = time()
        while time() - startTime <= RUNNINGTIME*60: #180 minutes
            if time() - lastImageTime >= TIMEBETWEENPHOTOS:
                imageCount = TakePicture(camera, imageCount)
                addCSVEntry(True, imageCount)
                lastImageTime = time()
            if time() - lastDataLogTime >= TIMEBETWEENDATALOGS:
                addCSVEntry(imgNum=imageCount)
                lastDataLogTime = time()
        
    Finish(camera)
    
main()
        


    
