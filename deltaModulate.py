##############################################################################################################################
# This program takes a starting image frame and the events recorded, performs delta modulation and displays the output
# Author: Ashish Rao M
# email: ashish.rao.m@gmail.com
##############################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
import cv2
import utils

def main():
    threshold = 0.61

    image = cv2.imread('video_images/frame0000.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = image.astype('float64')
    image = cv2.log(cv2.add(image, 1))
    #image = cv2.imread('data/slider_depth/images/frame_00000000.png')
    
    np.savetxt("CSV_files/image_init.csv", np.asarray(image),fmt='%i', delimiter=",")
    #read the first image (initial image) / assume it is log intensity

    events = utils.read_data('event_output/sim_events.txt')
    #events = utils.read_data('data/slider_depth/events.txt')

    for event in events:
        if event[3] == 1:
            image[int(event[1]), int(event[2])] -= threshold
        else:
            image[int(event[1]), int(event[2])] += threshold
            
    #add events to first image 
    image = np.exp(image).astype('uint8')
    cv2.imwrite('Images/final_frame_delta_mod.png', cv2.cvtColor(image,cv2.COLOR_GRAY2RGB))
    np.savetxt("CSV_files/image_final.csv", np.asarray(image),fmt='%i', delimiter=",")
    plt.title('Final frame of reconstruction')
    plt.imshow(image, cmap='gray')
    plt.show()
    
    #display last image(should be close to actual value)

if __name__ == '__main__':
    main()