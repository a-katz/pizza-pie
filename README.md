# pizza-pie
#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import numpy as np
import cv
import cv2
import time
def nothing(x):
	pass
def showit(img):
	cv2.imshow('camera', img)
	cv.GetTrackbarPos('thresh','control')
	ch = cv.WaitKey (2000)
	if (ch == 27 or ch == ord('q') or ch == ord('Q')):
		cv.DestroyAllWindows()
		exit()

cv.NamedWindow('camera', 1)
cv.NamedWindow('control')
cv2.imshow('control',Mat::zeros(1,500,cv2.CV_8UC1))
cv.CreateTrackbar('thresh','control',30,220,nothing)
capture = cv2.VideoCapture(1)
detector = cv2.SimpleBlobDetector()
while True:
	(ret, img) = capture.read()
	print img.shape
	red = img[:,:,2]
	showit(red) 
# Detect blobs.
	keypoints = detector.detect(red)
 	print keypoints
 	(ret,redbin) = cv2.threshold(red,200,255,cv2.THRESH_BINARY)
 	redbin = cv2.bitwise_not(redbin)
 	showit(redbin)
 	contours,img2 = cv2.findContours(redbin,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
 	for c in contours:
 		(x,y,w,h) = cv2.boundingRect(c)
 		if (w > 30 and h > 30 and x > 20 and y > 20):
 			cv2.rectangle(img,(x,y),(x+w,y+h),(128,80,200),3)
 			blobimg = redbin[x:x+w,y:y+h]
 			m = cv2.moments(blobimg)
 			hu = cv2.HuMoments(m)
 			print hu
 			print cv2.boundingRect(c)
 			
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
	print "blobs"
	showit(img)
	print "red"
	showit(red)
	
	
