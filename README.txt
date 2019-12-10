FaceDetection Project - Practicum I
Joel Vargas Jr. 

File Location on Raspberry Pi: 
/home/pi/Desktop/raspi-facetracking-master/pygameVideoDemo.py

New Installations:
Pygame
Tkinter

Worked with tkinter to incorporate a video framer using OpenCV with a tkinter GUI, but the issues included having to call objects and immediately stop calling the objects in order to have them show in a "view". Object in this regard was every text field and video frame.

I initally started with Pygame to build a GUI for the face recognition project. I was successful in making the GUI using a keyboard entries to toggle the program into a "Default" and "Show Data" view. I was also able to incorporate most of the code from the previous student. The only compenent that does not work correctly is the box tracking on the face due to "layering" issues that happen to be overwritten by a pygame screen update. In using pygame the biggest issue is learning how to only update certain elements in this project, in my case was the video frame to help with processing the video feed. The last issue is using OpenCV for the analytics because of its heavy use on the Raspberry Pi processor. Maybe a faster Pi will help in this regard. 