#!/usr/bin/python
import numpy as np
import cv
import cv2
import re, os, time
from random import randint

lasttime = None
frameCount = 0
animes = {}
aframe = {}
af = re.compile("([A-Za-z_]+)([0-9]+)\.png")

def loadAnimations() :
    global lasttime
    alist = []
    for f in sorted(os.listdir('./images')) :
        m = af.match(f)
        if (m) :
            thisfile = './images/' + f
            print "Adding " + m.group(1) +  " at position " + m.group(2)
            im = cv2.bitwise_not(cv2.imread(thisfile,0))
            if m.group(1) in animes.keys():
                animes[m.group(1)].append(im) # Add to list of images
            else :
                animes[m.group(1)] = [ im ]    # Create list with first image
                aframe[m.group(1)] = 0
    lasttime = time.time()
    return animes.keys()


def addImage(img, name, x, y) :
    global lasttime
    thistime = time.time()
    images = animes[name]
    if (thistime - lasttime > 0.1):
        aframe[name] = (aframe[name]+1)%len(images)
#        print str(aframe[name]) + "  of " + name + " numimages=" + str(len(images))
        lasttime = thistime
    (w,h) = images[aframe[name]].shape
    img[x:x+w,y:y+h,0] = cv2.add(images[aframe[name]],img[x:x+w,y:y+h,0])
    img[x:x+w,y:y+h,1] = cv2.add(images[aframe[name]],img[x:x+w,y:y+h,1])
    img[x:x+w,y:y+h,2] = cv2.add(images[aframe[name]],img[x:x+w,y:y+h,2])

def addSnow(img) :
    (w,h,planes) = img.shape
    for x in range(40) :
        for y in range(40) :
            rx = randint(1,w)
            rw = randint(2,5)
            ry = randint(1,h)
            rh = randint(2,5)
            for p in range(planes):
                img[rx:rx+rw,ry:ry+rh,p] = 200

def addRain(img) :
    (w,h,planes) = img.shape
    for x in range(30) :
        for y in range(30) :
            rx = randint(1,w)
            ry = randint(1,h)
            img[rx:rx+9,ry:ry+3,0] = 220
            img[rx:rx+9,ry:ry+3,1] = 180
            img[rx:rx+9,ry:ry+3,2] = 140
#            img[rx:rx+9,ry:ry+3,0] = cv2.add(200,img[rx:rx+9,ry:ry+3,0])
#            img[rx:rx+9,ry:ry+3,1] = cv2.add(100,img[rx:rx+9,ry:ry+3,1])
#            img[rx:rx+9,ry:ry+3,2] = cv2.add(100,img[rx:rx+9,ry:ry+3,2])
            

if __name__ == "__main__" :
    print "Main"
    cv2.namedWindow('camera',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('camera',500,600)
    cv2.moveWindow('camera',500,40)
    capture = cv2.VideoCapture(0)
    sprites = loadAnimations()
    offsets = {}
    offx = 100
    offy = 100
    for s in sprites:
        offsets[s] = (offx, offy)
        offy += 200
    raining_or_snowing = 0
    while(True) :
        for (x,y) in [(10,10),(20,20),(30,30),(40,45),(50,60),(70,80)] :
            raining_or_snowing += 1
            (ret, img) = capture.read()
            if (not ret) :
                continue
            for s in sprites:
                (ox, oy) = offsets[s]
                addImage(img, s, x+ox, y+oy)
            if ((raining_or_snowing % 100) < 30):
                pass
            elif ((raining_or_snowing % 100) < 70):
                addSnow(img)
            else :
                addRain(img)
            cv2.imshow('camera', img)
            cv.WaitKey(1)
            time.sleep(0.1)



