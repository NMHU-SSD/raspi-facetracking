import sys
import pygame
from pygame.locals import *
import cv2
import numpy as np
import face_recognition
import pickle
import os
import datetime
import time
#import Pi_Camera_Analytics
'''
sys.path.append('/home/pi/.local/lib/python3.5/site-packages/')
sys.path.append('/usr/local/lib/python3.5/dist-packages/')
sys.path.append('/usr/local/lib/python3.5/site-packages/')
'''

#GLOBAL FLAGS
global names_db
global encodings_db

def camera_feed():
    names_db=[]
    encodings_db=[]
    cascPath = "/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    white = (255,255,255)
    black = (0,0,0)
    xTop = 20


    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    pygame.init()
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode([1080,720])
    w,h = pygame.display.get_surface().get_size()
    vw = 640
    vh = 480

    first = True

    showData = False;


    while True:

        screen.fill([0,0,0]) #background color
        pygame.display.set_caption("Python Face Recogniton")
        font = pygame.font.Font("freesansbold.ttf", 32)
        
        font2 = pygame.font.Font("freesansbold.ttf", 24)
        text = font.render("New Mexico Highlands University", True, white, black)
        text2 = font2.render("Face Recognition Demo", True, white, black)
        
        #CHANGE X AND Y VARIABLES TO A DIFFERENT NAME (_x, _y) or (X, Y) (xPos, yPos)
 
        textRect = text.get_rect()
        _x = w / 2
        _y = 40
        textRect.center = (_x,_y)
        
        textRect2 = text.get_rect()
        _x = w / 2 + (textRect2.width/4)
        _y = 80 #new value for y
        textRect2.center = (_x,_y)

        screen.blit(text, textRect)
        screen.blit(text2, textRect2)
        
        _y+= 160
        #READING FROM CAMERA
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _rgb = rgb.swapaxes(0,1)
        _rgb = pygame.surfarray.make_surface(_rgb)


        ##WHEN PRESSING F1
        if showData == True:
            
            #DECTECT A FACE
            
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20,20)
            )
            
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []
            for encoding in encodings:
                matches = face_recognition.compare_faces(encodings_db, encoding)
                if True in matches:
                    #print("in true")
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    for i in matchedIdxs:
                        name = names_db[i]
                        counts[name] = counts.get(name, 0) + 1
                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)
                else:
                    #print("in false")
                    encodings_db.append(encoding)
                    ts = datetime.datetime.now()
                    names_db.append(str(ts))
                    name="I dont know you."
                    print(encodings_db)
                    print(names_db)
                names.append(name)
            
                
            #frame = cv2.flip(frame,0)
            
            #FOR TEXT
            _x = w/2 + vw
            text3 = font2.render("Face Recognition Data", True, white, black)
            textRect3 = text.get_rect()
            textRect3.center = (_x,_y)
            screen.blit(text3, textRect3)
            #FOR VIDEO
            _x = w/2 - vw #LEFT POSITION
            screen.blit(_rgb, (_x,_y))

            #figure out how to use _x for "frame"
           #DRAW BOX ON FACE
            font = cv2.FONT_HERSHEY_SIMPLEX

            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image
                cv2.rectangle(img, (left, top), (right, bottom),(0, 255, 0), 2)
                
                #faceRect = pygame.draw.rect(screen,(0,255,0),(top, right, bottom, left)) ################   UPDATED for everynew _x and _y based on key press F1
                y = top - 15 if top - 15 > 15 else top + 15

                #_faceRect = pygame.surfarray.make_surface(faceRect)

                cv2.putText(img, name, (left, y),font ,0.75,(0, 255, 0), 2)
                
            #cv2.imshow("Frame", rgb) ####

           
                
        else:
            _x = w/2 - vw/2 #VIDEO FRAME CENTERED
            screen.blit(_rgb, (_x,_y)) #x and y coords for the postion of the video frame

            #figure out how to use _x for "frame"
            #cv2.imshow("Frame", rgb)

        if first:
            pygame.display.update()
            first = False
        else:
            pygame.display.update(screen.blit(_rgb, (_x,_y)))
            #pygame.display.update(screen.blit(faceRect, (x,y)))

        for event in pygame.event.get(): #PRESS F1 TO TOGGLE BETWEEN DATA WINDOWS 
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_F1:
                    showData = not showData  #toggle
                    first = True
                elif event.key == pygame.K_ESCAPE: #PRESS ESCAPE TO END PROGRAM
                    pygame.quit()
                    cv2.destroyAllWindows()
                    sys.exit(0)
                    
                elif event.key == pygame.K_u:      #U key on keyboard for "Update"
                    #pygame.display.update(screen.blit(frame, (x,y)))
                    pygame.display.update()
                

                
def main():
    #create_data()
    #load_data()
    camera_feed()
    #test_time()


if __name__ == "__main__":
    main()

