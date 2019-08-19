


def init_phase_map(camera_dims):
  ''' 
    Function to define the intial size of the depth map matrix. Based on the size of the camera dimensions.

    Parameters:
    -----------
    camera_dims: <int tuple>
      Species resolution of the camera the event data comes from 

    Return:
    -------
    phase_map_list: <np.array of dimensions cam_width x cam_height with each index containing a list>
      Matrix of said dimensions containing empty lists at all positions
  '''
  phase_map_list = [[[] for j in range(camera_dims[1])] for i in range(camera_dims[0])] # investigate if this can be made a numpy array later(list need because need to average out noisy measurements may be there)
  return phase_map_list 

def compute_firing_rate(events, del_t, pixel_location):
  '''
    Compute and plot the firing rate of a particular pixel for a time interval defined by del_t. The pixel under observation is defined by the pixel_location. 
  
    Parameters:
    -----------
    events: <list> 
          List of event tuples

    del_t: <float>
            binning interval (in microseconds)

    pixel_location: <tuple> 
          Specify the location of the pixel whose firing rate has to be observed

    Return:
    --------
    firing_rates: <dict> 
      Dictionary of firing rates of all events for different time indices of resolution del_t starting from 0. 

    pos_firing_rates: <dict>
      Dictionary of firing rates of positive events for different time indices of resolution del_t starting from 0.

    neg_firing_rates: <dict>
      Dictionary of firing rates of negative events for different time indices of resolution del_t starting from 0.
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


def dict_single_pixel_events(events, pixel_location):
  '''
    Compute the firing rate of a particular pixel for a time interval defined by del_t. The pixel under observation is defined by the pixel_location. 

    Parameters:
    -----------
    events: <list> 
          List of event tuples

    pixel_location: <tuple> 
          Specify the location of the pixel which has to be observed

    Return:
    --------
    pixel_event_dict: <dict> 
      Dictionary of events happening at pixel location given in the input parameters 

  '''
  pixel_event_dict = dict()
  for event in events:
    if event[1]==pixel_location[1] and event[2]==pixel_location[0]:  
      if event[3] == 1:
        pixel_event_dict[event[0]] = event[3]
      else:
        pixel_event_dict[event[0]] = -1

  return pixel_event_dict

def dict_delta_mod_single_pixel_events(events, pixel_location, threshold):
  '''
    Compute the delta modulated signal for the pixel defined by the pixel_location. The delta in the delta modulation si defined by the threshold.

    Parameters:
    -----------
    events: <list> 
          List of event tuples

    pixel_location: <tuple> 
          Specify the location of the pixel which has to be observed
    
    threshold: <float>
          The delta value for the delta modulation reconstruction

    Return:
    --------
    delta_mod_pixel_event_dict: <dict> 
      Dictionary of delta modulated reconstruction happening at pixel location given in the input parameters 
  '''
  delta_mod_pixel_event_dict = dict()
  prev_value = 0
  for event in events:
    if event[1]==pixel_location[1] and event[2]==pixel_location[0]:  
      if event[3] == 1:
        delta_mod_pixel_event_dict[event[0]] = prev_value + threshold
      else:
        delta_mod_pixel_event_dict[event[0]] = prev_value - threshold
      prev_value = delta_mod_pixel_event_dict[event[0]]

  return delta_mod_pixel_event_dict