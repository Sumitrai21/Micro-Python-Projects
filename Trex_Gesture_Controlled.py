import cv2 as cv
import numpy as np
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,720)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

cv.namedWindow('frame')
cv.resizeWindow('frame',400,400)

region_of_interest_var = [(800,300),(1200,300),(1200,700),(800,700)]

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    channel_count = img.shape[2]
    match_mask_color = (255,) * channel_count
    cv.fillPoly(mask, vertices, match_mask_color)
    masked_img = cv.bitwise_and(img,mask)
    return masked_img

while True:
    

   
    
    masked_img1 = region_of_interest(frame1, np.array([region_of_interest_var], np.int32))
    masked_img2 = region_of_interest(frame2, np.array([region_of_interest_var], np.int32))
    

    diff = cv.absdiff(masked_img1, masked_img2)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh,None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x,y,w,h) = cv.boundingRect(contour)

        if cv.contourArea(contour) <2700:
            continue
        
        else:
            cv.rectangle(frame1,(800,300),(1200,700),(0,0,255),2)
            cv.putText(frame1,'Jump',(790,290),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            break

    #cv.drawContours(frame1, contours, -1,(0,255,0), 2)

    cv.rectangle(frame1,(800,300),(1200,700),(255,0,0),2)

    

    cv.imshow('frame', frame1)
    cv.imshow('masked_img', thresh)
    k = cv.waitKey(1) & 0xFF

    if k == 27:
        break

    frame1 = frame2
    _, frame2 = cap.read()




cap.release()
cv.destroyAllWindows()