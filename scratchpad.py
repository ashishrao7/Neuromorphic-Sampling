import cv2
import matplotlib.pyplot as plt
import numpy as np


'''vidcap = cv2.VideoCapture('videos/moving_pattern_for_sampling_exp.avi')
success,image = vidcap.read()
count = 0

while success:
  cv2.imwrite("test/frame%d.png" % count, image)

  img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  np.savetxt("image.csv", np.asarray(img),fmt='%i', delimiter=",")   
  break
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
'''

img = cv2.imread('sampling_pattern.png') 
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
np.savetxt("CSV_files/image.csv", np.asarray(img),fmt='%i', delimiter=",") 


