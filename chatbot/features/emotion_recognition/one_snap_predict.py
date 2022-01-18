#coding:utf-8

from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import os

# parameters for loading data and images
path2 = os.path.dirname(__file__)
detection_model_path = path2+'/haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = path2+'/models/_mini_XCEPTION.102-0.66.hdf5'

# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]
camera = cv2.VideoCapture(0)

def detect():

    #cv2.namedWindow('your_face')

    while True:
        frame = camera.read()[1]
    #reading the frame
        frame = imutils.resize(frame,width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
        canvas = np.zeros((250, 300, 3), dtype="uint8")
        frameClone = frame.copy()
        if len(faces) > 0:
            break

    if len(faces) > 0:
        faces = sorted(faces, reverse=True,
        key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
    (fX, fY, fW, fH) = faces
    # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
    # the ROI for classification via the CNN
    roi = gray[fY:fY + fH, fX:fX + fW]
    roi = cv2.resize(roi, (64, 64))
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)
    
    
    preds = emotion_classifier.predict(roi)[0]
    emotion_probability = np.max(preds)
    label = EMOTIONS[preds.argmax()]
    print(label)
    return emotion_probability, label


