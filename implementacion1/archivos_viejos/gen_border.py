# creamos el borde necesario para el algoritmo
import cv2
import numpy as np
import imutils

from matplotlib import pyplot as plt

# https://www.pyimagesearch.com/2014/10/20/finding-shapes-images-using-python-opencv/

mark = cv2.imread("mask_test.jpeg")
#image2 = np.zeros(image.shape, dtype=np.uint8)

# find all the 'black' shapes in the image
# lower = np.array([0, 0, 0])
# upper = np.array([15, 15, 15])
# shapeMask = cv2.inRange(image, lower, upper)

# cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
#
# for c in cnts:
# 	cv2.drawContours(image2, [c], -1, (255, 255, 255), 2)
#
# plt.imshow(image2, cmap="gray")
# plt.show()