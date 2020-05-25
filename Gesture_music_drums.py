import cv2 as cv
import numpy as np
import pygame

pygame.mixer.init()



cap = cv.VideoCapture(0)
ret, frame1 = cap.read()
ret, frame2 = cap.read()
k =0

while cap.isOpened():
    diff = cv.absdiff(frame1,frame2)

    gray = cv.cvtColor(diff,cv.COLOR_BGR2GRAY)

    vertices = [
        (50,50),
        (150,50),
        (150,150),
        (50,150)]

    vertices2 = [
        (500,50),
        (600,50),
        (600,150),
        (500,150)]

    vertices3 = [
        (300,50),
        (400,50),
        (400,150),
        (300,150)]

    vertices4 = [
        (50,300),
        (150,300),
        (150,400),
        (50,400)]

    vertices5 = [
        (500,300),
        (600,300),
        (600,400),
        (500,400)]


    mask = np.zeros_like(gray)
    match_mask_color = 255
    cv.fillPoly(mask,np.array([vertices],np.int32),match_mask_color)
    cv.fillPoly(mask,np.array([vertices2],np.int32),match_mask_color)
    cv.fillPoly(mask,np.array([vertices3],np.int32),match_mask_color)
    cv.fillPoly(mask,np.array([vertices4],np.int32),match_mask_color)
    cv.fillPoly(mask,np.array([vertices5],np.int32),match_mask_color)
    cv.rectangle(frame1,vertices[0],vertices[2],(0,0,255),1)
    cv.rectangle(frame1,vertices2[0],vertices2[2],(0,0,255),1)
    cv.rectangle(frame1,vertices3[0],vertices3[2],(0,0,255),1)
    cv.rectangle(frame1,vertices4[0],vertices4[2],(0,0,255),1)
    cv.rectangle(frame1,vertices5[0],vertices5[2],(0,0,255),1)
    masked_img = cv.bitwise_and(gray,mask)
    blur = cv.GaussianBlur(masked_img,(5,5), 0)
    _, thresh = cv.threshold(blur,20,255,cv.THRESH_BINARY)
    dilated = cv.dilate(thresh,None,iterations=3)
    contours,_ =cv.findContours(dilated,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        print(contour)
        (x,y,w,h) = cv.boundingRect(contour)
        if cv.contourArea(contour) < 1200:
            continue

        else:
            if x <100 and x>50 and y>50 and y<150:
                cv.putText(frame1,'Done',(x,y),cv.FONT_HERSHEY_COMPLEX,2,(0,0,255),1)
                cv.drawContours(frame1,contours,-1,(0,255,0),2)
                if k%3 == 0:
                    pygame.mixer.music.load('crash.mp3')
                    pygame.mixer.music.play()
                    break

                else:
                    k+=1


            elif x>500 and x<600 and y>50 and y<150:
                if k%3 ==0:
                    pygame.mixer.music.load('snare.mp3')
                    pygame.mixer.music.play()
                    break

                else:
                    k+=1

            
            elif x>300 and x<400 and y>50 and y<150:
                if k%5 ==0:
                    pygame.mixer.music.load('tom2.mp3')
                    pygame.mixer.music.play()
                    break

                else:
                    k+=1

            elif x>50 and x<150 and y>300 and y<400:
                if k%5 ==0:
                    pygame.mixer.music.load('tom1.mp3')
                    pygame.mixer.music.play()
                    break

                else:
                    k+=1

            elif x>500 and x<600 and y>300 and y<400:
                if k%5 ==0:
                    pygame.mixer.music.load('tom3.mp3')
                    pygame.mixer.music.play()
                    break

                else:
                    k+=1

            else:
                continue

 
    cv.imshow('mask',masked_img)
    cv.imshow('feed', frame1)
    frame1 = frame2
    _, frame2 = cap.read()
    if cv.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv.destroyAllWindows()