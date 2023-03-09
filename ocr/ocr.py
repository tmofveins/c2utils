import cv2
import pytesseract
from pytesseract import Output
import numpy as np

#################################################

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((2,2),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 500, 500)

def parse_image(img):
    ### seems like the best combo for c1 images
    img = get_grayscale(img)
    #img = remove_noise(img)
    #img = dilate(img)
    #img = erode(img)
    #img = opening(img)
    img = canny(img)
    #img = thresholding(img)

    draw_bounding_boxes(img)

    cv2.imwrite("test.png", img)

def draw_bounding_boxes(img):
    d = pytesseract.image_to_data(img, output_type = Output.DICT)

    n_boxes = len(d['text'])
    print(d['text'])

    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#################################################

img = cv2.imread("ocr/c1ocr_testing/image.png")
parse_image(img)