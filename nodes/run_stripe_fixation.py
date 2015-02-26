#!/usr/bin/env python
import rospy
import arena_experiments
import numpy as np
import time
import os

from phidgets_daq.msg import phidgetsDigitalOutput

def get_file_list(directory):
    cmd = 'ls ' + directory
    ls = os.popen(cmd).read()
    all_filelist = ls.split('\n')
    try:
        all_filelist.remove('')
    except:
        pass
    filelist = []
    for i, filename in enumerate(all_filelist):
        if 'Pattern' in filename:
            if 'stripe' not in filename:
                filelist.append(filename)
    return filelist
    
def choose_random_pattern():
    directory = '/home/caveman/Documents/panels_experiments/patterns'
    patterns = get_file_list(directory)
    print
    print patterns
    print
    pattern = None
    
    while pattern is None:
        randint = np.random.randint(0, len(patterns))
        pattern = patterns[randint]
        
    return randint, pattern


if __name__ == '__main__':
    rospy.init_node('experiment_controller')
    publish_to_daq_ssr = rospy.Publisher('/phidgets_daq/digital_output', phidgetsDigitalOutput, latch=True) 
    
    LEDArena = arena_experiments.LEDArena()
    
    LEDArena.run_closed_loop_pattern(5, ypos=0, pattern_name='stripe')
    
        
    
    
    

