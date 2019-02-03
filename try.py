import cv2
import numpy as np
import dlib
from math import hypot
import time
from flask import Flask,render_template
from win10toast import ToastNotifier
import tkinter as tk 
from PIL import ImageTk, Image
from tkinter import Label
from tkinter import Text
from tkinter import font

r = tk.Tk() 
r.title('EyeBlinkDetection')
#r.configure(background='white')


lbl = Label(r, text="B  L  I  N  K   A   B  I  T", font=("Times New Roman", 40))
lbl.grid(column=0, row=0)

lbl.pack()
img = Image.open("eye8.jpg")
img = img.resize((500,500), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img)

H=font.Font(family='Times New Roman', size = 20,weight='bold')
button1 = tk.Button(r, text='S  T  O  P', width=30,command = quit)
button1['font']=H
button1.pack(side=tk.BOTTOM)

 




panel = Label(r, image = img1)
panel.pack(side = "bottom", fill = "both", expand = "yes")



def fun():
    
    p=30
    q=100
  
 
    cap = cv2.VideoCapture(0)
    

    count=0
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat_2")
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:

        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            start=time.clock()
            landmarks = predictor(gray, face)
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks,frame)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks,frame)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
            cv2.putText(frame, str(time.clock()), (50, 150), font, 0.7, (0,0,255))
            if blinking_ratio > 5.7:
                    count=count+1
                    cv2.putText(frame, "Blink Count ="+str(count)+" "+str(time.clock()), (50, 150), font, 0.7, (0,0,255))
                    

            if (time.clock())>p and (count<q) :
                    cv2.putText(frame, "Blink your eyes ", (80, 180), font, 0.7, (0,0,255))
                    p=p+30
                    q=q+100
                    toaster=ToastNotifier()
                    toaster.show_toast("BLINK BLINK BLINKKKK")      
 
 
        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
 
    cap.release()
    cv2.destroyAllWindows()






 
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
 

 
def get_blinking_ratio(eye_points, facial_landmarks,frame):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
 
    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)
 
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
 
    ratio = hor_line_lenght / ver_line_lenght
    return ratio


H=font.Font(family='Times New Roman', size = 20,weight='bold')
button = tk.Button(r, text='S  T  A  R  T', width=30, command=fun)

button['font']=H

button.pack(side=tk.BOTTOM) 
r.mainloop() 




