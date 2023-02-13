import cv2
import pytesseract
import numpy as np

img = cv2.imread("ocr/c1ocr_testing/image.png", 0)
cv2.imwrite("test.png", img)