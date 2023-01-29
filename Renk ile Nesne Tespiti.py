# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 13:14:09 2023

@author: muhar
"""

import cv2
import numpy as np 
from collections import deque



buffer_size = 16
pts = deque(maxlen = buffer_size)



cap = cv2.VideoCapture(0)
cap.set(3,960)
cap.set(4,480)

def callback(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')

ilowH = 0
ihighH = 179
ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255


cv2.createTrackbar('lowH','image',ilowH,179,callback)
cv2.createTrackbar('highH','image',ihighH,179,callback)

cv2.createTrackbar('lowS','image',ilowS,255,callback)
cv2.createTrackbar('highS','image',ihighS,255,callback)

cv2.createTrackbar('lowV','image',ilowV,255,callback)
cv2.createTrackbar('highV','image',ihighV,255,callback)


while True:
    ret, frame = cap.read()
    ilowH = cv2.getTrackbarPos('lowH', 'image')
    ihighH = cv2.getTrackbarPos('highH', 'image')
    ilowS = cv2.getTrackbarPos('lowS', 'image')
    ihighS = cv2.getTrackbarPos('highS', 'image')
    ilowV = cv2.getTrackbarPos('lowV', 'image')
    ihighV = cv2.getTrackbarPos('highV', 'image')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imshow('hsv', hsv)
    lower_hsv = np.array([ilowH, ilowS, ilowV])
    higher_hsv = np.array([ihighH, ihighS, ihighV])
    mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
    print (ilowH, ilowS, ilowV)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    
    success, imgOriginal = cap.read()
    
    if success:
        
        
        blurred = cv2.GaussianBlur(imgOriginal,(11,11),0 )
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
        cv2.imshow("mask Image", mask)
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None,iterations = 2)
        cv2.imshow("Mask + erozyon ve genişleme", mask)
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None
        
        if len(contours) > 0:
            c = max(contours, key = cv2.contourArea)
            rect = cv2.minAreaRect(c)
            ((x,y), (width, height), rotation ) = rect
            s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            print(s)
            A=12.2316513
            print(np.round(A))
            
            box = cv2.boxPoints(rect)
            box = np.int64(box)
            
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            
            cv2.drawContours(imgOriginal, [box], 0, (0,255,255),2)
            cv2.circle(imgOriginal, center, 5, (255,0,255),-1)
            
            cv2.putText(imgOriginal, s, (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (255,255,255),2)

            pts.appendleft(center)
            
            for i in range(1, len(pts)):
                
                if pts[i-1] is None or pts[i] is None: continue
                    
                cv2.line(imgOriginal, pts[i-1], pts[i], (0,255,0),3)
        cv2.imshow("Orijinal Tespit", imgOriginal)
            
    if cv2.waitKey(1) & 0xFF == ord("q"): break
        
    
    
    
    
    
    
    
    
    
    
    
