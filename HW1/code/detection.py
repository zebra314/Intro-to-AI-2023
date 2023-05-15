import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import datetime

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    cwd = os.getcwd()
    filePath = cwd + '/' 

    file_info = []
    face_all = []
    face_in_single_file = []
    
    # Extract the text from the .txt file
    with open(filePath + dataPath) as f:
      for line in f.readlines():
        element = line.split()
        if len(element) == 4:
          face_in_single_file.append(element)
        elif len(element) == 2 and len(face_in_single_file) == 0:
          file_info.append(element)
        else:
          file_info.append(element)
          face_all.append(face_in_single_file)
          face_in_single_file = []
      face_all.append(face_in_single_file)
    
    # Detect the face and plot the bounding box 
    for info, faces in zip(file_info, face_all):
      name, num = info[0], int(info[1])
      img = cv2.imread(filePath + 'data/detect/' + name)
      for i in range(0, num):
        x, y, w, h = int(faces[i][0]), int(faces[i][1]), int(faces[i][2]), int(faces[i][3])
        face = img[y:y+h, x:x+w]
        face = cv2.resize(face, (19, 19), interpolation=cv2.INTER_AREA)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        color = (0,255,0) if clf.classify(face) == 1 else (0,0,255)
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2, cv2.LINE_AA)
      cv2.imshow(name, img)
    cv2.waitKey(0)
    # End your code (Part 4)
        


    


           
