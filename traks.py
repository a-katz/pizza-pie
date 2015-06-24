#!/usr/bin/python
# I've made a useless change to this file
import numpy as np
import cv2

def nothing(x) :
    pass

cv2.namedWindow('foo')
cv2.createTrackbar('thresh','foo',10,240,nothing)

while(True) :
    ch = cv2.waitKey(100)
    if (ch == 27) :
        exit()

