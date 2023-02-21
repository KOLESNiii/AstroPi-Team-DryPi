from pathlib import Path
import cv2
import numpy as np
from fastiecm import fastiecm
from os import makedirs

PROGRAMPATH = Path(__file__).parent.resolve() #path to this file

def increase_contrast(img):
    input_min = np.percentile(img, 5)
    input_max = np.percentile(img, 95)

    output_min = 0.0
    output_max = 255.0

    output = img - input_min
    input_difference = (input_min - input_max)
    if input_difference == 0:
        input_difference = 0.0000001 #avoid division by zero
    output *= ((output_min - output_max) / input_difference)
    output += input_min

    return output

def display(img, title):
    img = np.array(img, dtype=float) / float(255)
    shape = img.shape
    height = int(shape[0]/2)
    width = int(shape[1]/2)
    img = cv2.resize(img, (width, height))
    cv2.namedWindow(title)
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ndvi(img):
    b, g, r = cv2.split(img)
    bottom = b.astype(float) + r.astype(float)
    bottom[bottom==0] = 0.0000001 #avoid division by zero
    ndvi = (b.astype(float) - r) / bottom

    return ndvi

def colour_map(img):
    img = img.astype(np.uint8)
    img = cv2.applyColorMap(img, fastiecm)
    return img

def convert_all(path):
    img = cv2.imread(path)
    #display(img, f'Original {path[-9:-4]}')
    changed = increase_contrast(img)
    #display(changed, f'Contrast {path[-9:-4]}')
    ndvi_image = ndvi(changed)
    ndvi_contrast = increase_contrast(ndvi_image)
    #display(ndvi_contrast, f'NDVI {path[-9:-4]}')
    ndvi_colour = colour_map(ndvi_contrast)
    #display(ndvi_colour, f'NDVI Coloured {path[-9:-4]}')
    makedirs(f'{PROGRAMPATH}\images_testing_converted\\', exist_ok = True)
    cv2.imwrite(f'{PROGRAMPATH}\images_testing_converted\\ndvi_{path[-9:-4]}.jpg', ndvi_colour)

for image in PROGRAMPATH.glob('images_testing/*.jpg'):
    convert_all(str(image))


