import cv2
import pytesseract
import numpy as np

img = cv2.imread("ocr/c1ocr_testing/image.png")
cv2.imshow("img", img)
cv2.waitKey(0)