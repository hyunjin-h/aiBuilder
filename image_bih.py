import cv2
import numpy as np

img = cv2.imread('image/dalle.png')
height, width = img.shape[:2]

#--② 배율 지정으로 확대
dst2 = cv2.resize(img, None,  None, 2, 2, cv2.INTER_CUBIC)
cv2.imshow("big", dst2)
cv2.imwrite('image/dalleBig.png',dst2)