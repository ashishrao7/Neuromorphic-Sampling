#######################################################################################
# This is a utility library for common methods 
# Author: Ashish Rao M
# email: ashish.rao.m@gmail.com
#######################################################################################
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

    Parameters:
    -----------
    path: <string>
      The location of data to be read from
    
    Return:
    -------
    events: <list>
      A list of events read from the file 
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
  '''
    This function creates a new file. That's all!
  '''
  f= open(filename,"w+")
  return f

def append_to_event_file(file, event):
  '''
    This function is as useless as the earlier function. I don't know what i was thinking
  '''
  file.write(event)
  

def convert_to_xyz_and_store(filename, depth_map_matrix):
  '''
    Convert the depth map values to xyz file and store in the current directory
    
    Parameters:
    -----------
    filename: <string> 
      Name of the file to be saved

    depth_map_matrix: <np.array>
      Matrix containing depth values at all position of the image
  '''
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
  
    Parameters:
    -----------
    depth_map: <np.array>
      Matrix containing depth values at all positions of the image
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
  return image, plt

def plot_dictionary(data, title, xlimits, xlabel, ylabel, type='default'):
  '''
    Plot the values of a dictionary

    Parameters:
    -----------
    data: <dict>
      The dictionary to be plotted
    
    title: <string>
      Yeah you know what this means. why are you even reading this
    
    xlimits: <list>
      The start and stop values on the x axis
    
    xlabel: <string>
      Seriously?

    ylabel: <string>
      Seriously? Seriously?
    
    type: <string>
      To make different types of plots. Currently only stem and linear interpolation have been implemented 
  
  '''
  lists = sorted(data.items()) # sorted by key, return a list of tuples
  x, y = zip(*lists) 
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.xlim(xlimits)
  plt.ylim(min(y) - 1 , max(y) + 1)
  if type=='stem':
    plt.stem(x, y)
  elif type=='step':
    plt.step(x, y)
  else:
    plt.plot(x, y)

  plt.savefig('plots/' + title + '.png')
  plt.show()

def compare_plots(dict1, dict2, label_1, label_2):
  '''
    Plot two dictinaries simultaenuosly 

    Parameters:
    -----------
    dict1: <dict>
      The dictionary 1 to be plotted
    
    dict2: <dict>
      The dictionary 2 to be plotted
    
    label_1: <string>
      The name of the label 1
    
    label_2: <string>
      The name of the label 2
  '''
  fig, ax1 = plt.subplots()
  lists = sorted(dict1.items()) # sorted by key, return a list of tuples
  x, y = zip(*lists) 
  color = 'tab:green'
  ax1.set_xlabel('time (s)')
  ax1.set_ylabel(label_1, color=color)
  ax1.step(x, y, color=color, where='post')
  ax1.tick_params(axis='y', labelcolor=color)

  ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

  lists = sorted(dict2.items())
  x, y = zip(*lists) 
  color = 'tab:blue'
  ax2.set_ylabel(label_2, color=color)  # we already handled the x-label with ax1
  ax2.stem(x, y, color=color)
  ax2.tick_params(axis='y', labelcolor=color)
  
  fig.tight_layout()  # otherwise the right y-label is slightly clipped
  plt.show()

def plot_multiple_dictionaries(*dicts):
  '''
    Plots in a column multiple dictionaries separately

    Parameteres:
    -----------
    *dict: <list of dicts>
      List of dictionaries to be plotted
  '''
  fig = plt.figure(1)
  
  ax = fig.add_subplot(len(dicts), 1, 1)
  ax.set_xlabel('time (s)')
  ax.set_ylabel('Intensity')
  lists = sorted(dicts[0].items()) # sorted by key, return a list of tuples
  x, y = zip(*lists) 
  ax.plot(x,y)

  ax = fig.add_subplot(len(dicts), 1, 2)
  ax.set_xlabel('time (s)')
  ax.set_ylabel('Log Intensity')
  
  lists = sorted(dicts[1].items()) # sorted by key, return a list of tuples
  x, y = zip(*lists) 
  ax.set_xlim([0, x[-1]])
  ax.step(x,y, where='post')

  ax = fig.add_subplot(len(dicts), 1, 3)
  ax.set_xlabel('time (s)')
  ax.set_ylabel('Event Data')
  lists = sorted(dicts[2].items()) # sorted by key, return a list of tuples
  x, y = zip(*lists) 
  ax.set_xlim([0, x[-1]])
  ax.stem(x,y)

  fig.tight_layout()
  plt.show()
  
def make_video(image_folder, video_name=''):  
  '''
  Make video from images. 

  Parameters:
  ----------
  image_folder: <string>
    directory of the folder containing the images
  '''
  
  if video_name=='':
    video_name = 'videos/event_simulation.avi'

  images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
  frame = cv2.imread(os.path.join(image_folder, images[0]))
  height, width, layers = frame.shape

  video = cv2.VideoWriter(video_name, 0, 24, (width,height))

  for image in images:
      video.write(cv2.imread(os.path.join(image_folder, image)))
  cv2.destroyAllWindows()
  video.release()

def read_intensity_at_location(location, data_folder, images_text_file=None, frame_rate=24, log='no'):
  '''
  Creates a dictionary of time vs intensity at a particular pixel location
  
  Parameter:
  ----------

  location:<int tuple>
    Coordinates of the pixel

  data_folder:<string>
    Directory from where the images are read
  
  images_text_file:<string>
    Name of the file which containes names of the images
  
  frame_rate:<int>
    Frame rate at which all images have been captured
  
  log: <boolean>
    Yes if the images captured are in the log intensity 
  
  Return:
  -------
  image_dict:<dict>
    dictionary of time vs intensity
  '''
  time = 0
  image_dict = dict()
  if log=='no':
    if images_text_file:
      file = open(images_text_file, "r")
      print('Reading image timestamps')
      information = [list(line.split()) for line in file]
      file.close()
      for row in information:
        image = cv2.imread(data_folder+row[1])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_dict[float(row[0])] = image[location[0], location[1]]

    else:
      # this part of  function not working properly check it later
      images = [img for img in os.listdir(data_folder+'images/') if img.endswith(".png")]
      images = sorted(images) 
      for image in images:
        image = cv2.imread(data_folder+'images/'+image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(image.shape)
        image_dict[time] = image[location[0], location[1]]
        time+= frame_rate

  elif log=='yes':
      if images_text_file:
        file = open(images_text_file, "r")
        print('Reading image timestamps')
        information = [list(line.split()) for line in file]
        file.close()
        for row in information:
          image = cv2.imread(data_folder+row[1])
          image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          image_dict[float(row[0])] = np.log(np.add(image[location[0], location[1]], 0.001))
    
  return image_dict
