import cv2
import pytesseract
import numpy as np

img = cv2.imread("ocr/c1ocr_testing/image.png")

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

### seems like the best combo for c1 images

img = get_grayscale(img)
img = thresholding(img)

cv2.imwrite("test.png", img)