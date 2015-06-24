#!/usr/bin/python
from Tkinter import *
import numpy as np
import cv
import cv2
import time

class Blob:

    def __init__(self, master):
        self.display = 1
        self.img = None
        self.red = None
        self.redbin = None
        self.capture = None
        self.root = master
        cv2.namedWindow('camera',cv2.WINDOW_NORMAL)
        cv2.createTrackbar('thresh','camera',10,240,self.on_threshold)
        cv2.createTrackbar('minimum','camera',30,100,self.on_threshold)
        cv2.createTrackbar('maximum','camera',300,800,self.on_threshold)
        self.capture = cv2.VideoCapture(0)
        self.makeControl()
        self.next_picture()

    def toggleDisplay(self) :
        if (self.display == 1) :
            self.display = 0
        else :
            self.display = 1
        
    def makeControl(self) :
        self.frame = Frame(self.root)
        self.frame.pack()
        self.button = Button(self.frame, 
                             text="QUIT", fg="red",
                             command=self.frame.quit)
        self.button.pack(side=LEFT)
        self.toggle = Button(self.frame,
                             text="Toggle Display",
                             command=self.toggleDisplay)
        self.toggle.pack(side=LEFT)


    def show_image(self):
        cv2.imshow('camera', self.red)

    def quitKey(self) :
        ch = ( cv.WaitKey(10) % 256 )
        if (   ch == 27
            or ch == ord('x')
            or ch == ord('X')
            or ch == ord('q')
            or ch == ord('Q') ) :
            print "Quitting"
            self.frame.quit()

    def next_picture(self):
	th = cv.GetTrackbarPos('thresh','camera')
	(ret, self.img) = self.capture.read()
	if (ret) :
            self.red = self.img[:,:,2]
            (ret,rbin) = cv2.threshold(self.red,th,255,cv2.THRESH_BINARY)
            if (ret) :
                self.redbin = cv2.bitwise_not(rbin)
                saveBinary = np.copy(self.redbin)
                blobs = self.getBlobs(self.redbin)
                if (self.display == 1) :
                    self.outlineBlobs(saveBinary, blobs)
                    cv2.imshow('camera', saveBinary)
                else :
                    self.outlineBlobs(self.img, blobs)
                    cv2.imshow('camera', self.img)
                self.quitKey()
        else :
            print "Dropped Frame"
        self.root.after(300, self.next_picture)

    def on_threshold(self,th):
        pass

    def showHu(blob):
        m = cv2.moments(blob)
        hu = cv2.HuMoments(m)
        print hu

    def outlineBlobs(self,image,blobs): # Purple rectangle wid=3
        for ((x,y,w,h),_) in blobs:
            cv2.rectangle(image,(x,y),(x+w,y+h),(128,80,200),3)

    def write_slogan(self):
        print "Tkinter is easy to use!"

    # Blobs are (BBox,Image) tuples where BBox is (x,y,w,h)
    def getBlobs(self,binImg):  # Detect blobs.
        blobs = []
        ( contours, img2 ) = cv2.findContours(binImg,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	minBlob = cv.GetTrackbarPos('minimum','camera')
	maxBlob = cv.GetTrackbarPos('maximum','camera')
        for c in contours :
            (x,y,w,h) = cv2.boundingRect(c)
            # Filter for  minimum and maximum size
            if ( w > minBlob and h > minBlob and w < maxBlob and h < maxBlob ):
                        blobs.append(( cv2.boundingRect(c),
                                       binImg[x:x+w,y:y+h]))
        return blobs


root = Tk()
blobApp = Blob(root)
root.mainloop()

	
	
