#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import os 

if __name__ == '__main__':

    from sys import argv, exit
    import cv2 as cv2
    import numpy as np
    from numpy import size, uint8, zeros, save
    from time import time
    import utils
    import os
    
    height = 260
    width = 346
    savevid = True
    threshold = 14
    event_file = utils.create_new_event_file('event_output/sim_events.txt')

# initialise the video capture
    img_src = sys.argv[1]  # inbuilt camera
    images_names = [img_name for img_name in os.listdir(img_src) if img_name.endswith(".png")]
    images_names.sort()
    
    if images_names:
        img = cv2.imread(img_src + '/' + images_names[0])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bg = cv2.flip(img, 1).astype('float64')
        #bg = cv2.log(cv2.add(bg, 1))
        native_width = size(img, 1)  # get native frame width
        native_height = size(img, 0)  # get native frame height
    
    frame = 0

    for img_name in images_names:
        # get a frame
        img = cv2.imread(img_src + '/' + img_name)

        # make image greyscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        # flip it so it behaves like a mirror
        img = cv2.flip(img, 1).astype('float64')
        
        # logarithmic compression (log(1.0 + I))
        
        #img = cv2.log(cv2.add(img, 1))

        # calculate difference with background
        dif = cv2.subtract(img, bg)
        
        # detect on and off events
        on = cv2.compare(dif, threshold, cv2.CMP_GT)
        off = cv2.compare(-1.0 * dif, threshold, cv2.CMP_GT)
        
        if savevid:
            frame += 1
        
        # spatial filter image
        bgnew = cv2.GaussianBlur(img, (0, 0), 0 + 0.00001)
        bgnew = img
        
        # update background via temporal LPF
        cLPF = 0
        bg = cv2.add(cLPF * bg, (1 - cLPF) * bgnew)
        
        # create image
        gray = 125*np.ones([height, width], dtype=uint8)
        t = time()
        gray[off>0] = 0
        gray[on>0] = 255

        

        pos_coords = np.where(on)
        if pos_coords:
            for x,y in zip(pos_coords[0], pos_coords[1]):
                event = '{} {} {} 1 \n'.format(t, x, y)
                utils.append_to_event_file(event_file, event)

        
        neg_coords = np.where(off)
        if neg_coords:
            for x,y in zip(neg_coords[0], neg_coords[1]):
                event = '{} {} {} 0 \n'.format(t, x, y)
                utils.append_to_event_file(event_file, event)
       
        cv2.imwrite('event_output/event_frames/' + str(frame).zfill(3)+'.png',cv2.flip(gray,1).astype('uint8'))

    
    event_file.close() #close event file
    utils.make_video('event_output/event_frames/')

    print('DONE!')
