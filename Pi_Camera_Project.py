import sys

sys.path.append('/home/pi/.local/lib/python3.5/site-packages/')
sys.path.append('/usr/local/lib/python3.5/dist-packages/')
sys.path.append('/usr/local/lib/python3.5/site-packages/')

import numpy as np
import cv2
import face_recognition
import pickle
import os
import datetime
import time

global names_db
global encodings_db



def camera_stream():
    names_db=[]
    encodings_db=[]
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    #cap.set(3, 640)  # set Width
    #cap.set(4, 480)  # set Height
    while True:
        time.sleep(0.1)
        ret, img = cap.read()
        img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(encodings_db, encoding)
            if True in matches:
                print("in ture")
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
                print("in false")
                encodings_db.append(encoding)
                ts = datetime.datetime.now()
                names_db.append(str(ts))
                name="i dont Know you"
                print(encodings_db)
                print(names_db)
            names.append(name)                                
        font = cv2.FONT_HERSHEY_SIMPLEX
        for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
            cv2.rectangle(img, (left, top), (right, bottom),(0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(img, name, (left, y),font ,0.75,(0, 255, 0), 2)
        cv2.imshow("Frame", img)
        key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break


    cap.release()
    cv2.destroyAllWindows()


    
def load_data():
    global names_db
    global encodings_db
    try:
        with open('encodings','rb')as pickle_file:
            encodings_db = pickle.load(pickle_file)
        with open('name','rb')as pickle_files:
            names_db = pickle.load(pickle_files)
        print("Data Object loaded")
        #print(names_db)
        #print(encodings_db)
    except IOError:
        print("cant load data from disk... creating New One") 
        create_data()


def create_data():
    global names_db
    global encodings_db
    knownEncodings=[]
    knownNames=[]
    

def write_data(names,encodings):
    try:
        f=open("name","wb")
        f.write(pickle.dumps(names))
        f.close
        m=open("encodings","wb")
        m.write(pickle.dumps(encodings))
        m.close
    except IOError:
        print("Cant write data to disk")


def test_time():
    ts = datetime.datetime.now()
    print(ts)



    
def main():
    #create_data()
    #load_data()
    camera_stream()
   #test_time()
    #


if __name__ == "__main__":
    main()
