################ Face detection using ROI and template masking ###########################3

import cv2 as cv
import numpy as np

def nothing(x):
    pass


cap = cv.VideoCapture(0)
cv.namedWindow('capture Image')
cv.createTrackbar('capture','capture Image',0,1,nothing)

k = 0
mask = 0
while cap.isOpened():
    _, frame  = cap.read()
    _, frame2 = cap.read()

    if k == 0:
        r = cv.selectROI('frame',frame)
        mask = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        mask = cv.cvtColor(mask,cv.COLOR_BGR2GRAY)
        cv.imshow('frame', frame)
        k=1

    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    
    template_matching = cv.matchTemplate(gray,mask,cv.TM_CCORR_NORMED)

    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(template_matching)
    print(minLoc,maxLoc)
    print(maxVal)
    if maxVal > 0.947:
        cv.rectangle(frame,(maxLoc),(maxLoc[0]+150,maxLoc[1]+150),(0,0,255),1)
        cv.putText(frame,'MASK ON',maxLoc,cv.FONT_HERSHEY_COMPLEX,2,(255,22,0),2)

    cv.imshow('frame', frame)
    cv.imshow('template', template_matching)

    if cv.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv.destroyAllWindows()