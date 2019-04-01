


def init_phase_map(camera_dims):
  ''' 
    Function to define the intial size of the depth map matrix. Based on the size of the camera dimensions.
  '''
  phase_map_list = [[[] for j in range(camera_dims[1])] for i in range(camera_dims[0])] # investigate if this can be made a numpy array later(list need because need to average out noisy measurements may be there)
  return phase_map_list 

def compute_firing_rate(events, del_t, pixel_location):
  '''
    Compute and plot the firing rate of a particular pixel for a time interval defined by del_t. The pixel under observation is defined by the pixel_location. 
  
  Parameters:
  -----------
  events<list> :
         List of event tuples

  del_t<float>: 
          binning interval (in microseconds)

  pixel_location<tuple>: 
          Specify the location of the pixel whose firing rate has to be observed

  Return:
  --------
  firing_rates<> : 
  '''

  
  time, rate, pos_firing_rate, neg_firing_rate = events[0][0], 0, 0, 0
  
  firing_rates = dict()
  pos_firing_rate_dict = dict()
  neg_firing_rate_dict = dict()

  for event in events:
    if event[1]==pixel_location[1] and event[2]==pixel_location[0]:   
      print(event)
      if event[0] < (time + del_t):
        
        if event[3] == 1:
          pos_firing_rate+= 1
        else:
          neg_firing_rate+= 1
        
        rate += 1
      
      else:
        print(rate)
        firing_rates[time] = rate # assign to previous bin or to current bin??
        pos_firing_rate_dict[time] = pos_firing_rate
        neg_firing_rate_dict[time] = neg_firing_rate
        
        #reset counters and move to next time bin
        rate, pos_firing_rate, neg_firing_rate = 0, 0, 0
        time = time + del_t

        if  event[0] < (time + del_t):
          if event[3] == 1:
            pos_firing_rate+= 1
          else:
            neg_firing_rate+= 1
        
          rate += 1
        
  print(rate)

  #assigment for the last time bin
  firing_rates[time] = rate 
  pos_firing_rate_dict[time] = pos_firing_rate
  neg_firing_rate_dict[time] = neg_firing_rate

  return firing_rates, pos_firing_rate_dict, neg_firing_rate_dict


def compute_phase_change(event, depth_map, scan_speed, start_time, focal_length, baseline):
  '''
      compute phase change at each pixel in the imager due to moving patterns which generate events at varying rates
  '''
  
  time, y, x, _ = event #x and y are interchanged because the convention followed is different in code and in the dvs_drivers
  
  pass


def dict_single_pixel_events(events, pixel_location):
  time = events[0][0]
  pixel_event_dict = dict()
  for event in events:
    if event[1]==pixel_location[1] and event[2]==pixel_location[0]:  
      if event[3] == 1:
        pixel_event_dict[event[0]] = event[3]
      else:
        pixel_event_dict[event[0]] = -1

  return pixel_event_dict

  pass

def unwrap_phase():
  pass

def get_wrapped_phase_map(events, phase_map):

  pass 

