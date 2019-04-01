
import numpy as np 
import matplotlib.pyplot as plt
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import os
import cv2


def read_data(path):
  '''
    Function to read data from the file containing events
  '''
  file = open(path, "r")
  print('Reading events from file ')
  events = [list(map(float,line.split())) for line in file]
  start_time = events[0][0]
  file.close()
  print('Events have been read!')
  events = np.array(events, dtype=np.float_)
  events[: , 0] = events[:, 0] - start_time 
  return events

def create_new_event_file(filename):
  f= open(filename,"w+")
  return f

def append_to_event_file(file, event):
  file.write(event)
  

def convert_to_xyz_and_store(filename, depth_map_matrix):
  f = open(filename,"w+")
  for x in tqdm(range(depth_map_matrix.shape[0])):
    for y in range(depth_map_matrix.shape[1]):
      f.write("{}\t{}\t{}\n".format(x, y, depth_map_matrix[x][y]))
  num_lines = sum([1 for line in f])
  f.close()
  print('finished preparing {}. The file has {} lines'.format(filename, num_lines))


def plot_depth_map(depth_map):
  '''
   Plot image of the final depth map numpy array
  '''
  plt.title('Depth Map from Structured lighting')
  plt.ylabel('Camera y co-ord')
  plt.xlabel('Camera x co-ord')
  plt.xlim(0, 345)
  plt.ylim(0, 259)
  image = (depth_map < 100)*depth_map
  image = (image > 15)*depth_map
  image[image==0] = 100
  image = ndimage.rotate(image, 180)  
  plt.imshow(image, cmap ='rainbow')
  plt.colorbar().ax.set_ylabel('depth in cm', rotation=270)
  plt.show()
  print("Plotted Depth Map")
  return image

def plot_dictionary(data, title, xlimits, xlabel, ylabel, type='default'):
  lists = sorted(data.items()) # sorted by key, return a list of tuples
  x, y = zip(*lists) 
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.xlim(xlimits)
  plt.ylim(min(y) - 1 , max(y) + 1)
  if type=='stem':
    plt.stem(x, y)
  else:
    plt.plot(x, y)

  plt.savefig('plots/' + title + '.png')
  plt.show()
  
def make_video(image_folder):  
  video_name = 'videos/event_simulation.avi'

  images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
  frame = cv2.imread(os.path.join(image_folder, images[0]))
  height, width, layers = frame.shape

  video = cv2.VideoWriter(video_name, 0, 30, (width,height))

  for image in images:
      video.write(cv2.imread(os.path.join(image_folder, image)))
  cv2.destroyAllWindows()
  video.release()