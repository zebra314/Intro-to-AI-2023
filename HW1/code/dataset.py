import os
import cv2
import numpy as np

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    cwd = os.getcwd()
    dataPath = cwd + '/'+ dataPath
    dataset = []
    
    for directory in os.listdir(dataPath):
      for file in os.listdir(dataPath + '/' + directory):
        img = cv2.imread(dataPath + '/' + directory + '/' + file, cv2.IMREAD_GRAYSCALE)
        data = (np.array(img), 1 if directory == 'face' else 0)
        dataset.append(data)
    return dataset
    # End your code (Part 1)
