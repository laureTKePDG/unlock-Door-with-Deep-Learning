# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 10:02:24 2024

@author: jk
"""
import cv2
import face_recognition
import numpy as np
from os import listdir
from os.path import isfile, join
import serial
import time
import pyttsx3

q = 1
x = 0
c = 0
m = 0
d = 0

while q <= 2:
    data_path = 'C:/Users/jk/Porte-recognition/image/'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    Training_data, Labels = [], []
    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        images = face_recognition.load_image_file(image_path)
        images_encoding = face_recognition.face_encodings(images)[0]
        Training_data.append(images_encoding)
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)
    model = face_recognition.LinearSVC()
    model.fit(Training_data, Labels)
    print("training complete")
    q += 1

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 140)
engine.setProperty("volume", 1000)

def face_detector(img, size=0.5):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_img)
    if not face_locations:
        return img, []

    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 255), 2)
        roi = img[top:bottom, left:right]
        roi = cv2.resize(roi, (200, 200))

    return img, roi

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    image, face = face_detector(frame)

    try:
        face_encoding = face_recognition.face_encodings(face)[0]
        result = model.predict([face_encoding])[0]
        if result < 500:
            confidence = int((1 - (result) / 300) * 100)
            display_string = str(confidence)
            cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 0))

        if confidence >= 83:
            cv2.putText(image, "unlocked", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
            cv2.imshow('face', image)
            x += 1
        else:
            cv2.putText(image, "locked", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
            cv2.imshow('face', image)
            c += 1
    except:
        cv2.putText(image, "Face not found", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
        cv2.imshow('face', image)
        d += 1
        pass

    if cv2.waitKey(1) == 13 or x == 10 or c == 30 or d == 20:
        break

cap.release()
cv2.destroyAllWindows()

if x >= 5:
    m = 1
    ard = serial.Serial('com3', 9600)
    time.sleep(2)
    var = 'a'
    c = var.encode()
    speak("Face recognition complete..it is matching with database...welcome..sir..Door is opening for 5 seconds")
    ard.write(c)
    time.sleep(4)
elif c == 30:
    speak("face is not matching..please try again")
elif d == 20:
    speak("face is not found please try again")

if m == 1:
    speak("door is closing")
