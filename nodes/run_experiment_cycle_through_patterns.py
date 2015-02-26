#!/usr/bin/env python
import rospy
import arena_experiments
import numpy as np
import time
import os

from phidgets_daq.msg import phidgetsDigitalOutput
from std_msgs.msg import String
import csv

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
    
def choose_random_pattern(directory):
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
    publish_pattern_name = rospy.Publisher('/ledpanels/pattern', String, queue_size=3)
    
    ## write pattern name and id correspondence
    pattern_to_id_filename = time.strftime("%Y%m%d_%H_%M_%S_ledpanel_pattern_ids.csv", time.localtime())
    print 'pattern id filename: ', pattern_to_id_filename
    csvfile = open(os.path.expanduser(pattern_to_id_filename), 'w')
    datawrite = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    row = []
    patterns_directory = '/home/caveman/Documents/panels_experiments/patterns'
    patterns = get_file_list(patterns_directory)
    for i, pattern in enumerate(patterns):
        datawrite.writerow([i, pattern])
    csvfile.close()
    ##
    
    LEDArena = arena_experiments.LEDArena()
    
    trial_length = 30
    number_of_trials = 10
    number_of_trials_done = 0
    stripe_fixation_length = 30
    
    topics = ['/phidgets_daq/frequency', 
              '/phidgets_daq/left_amp',
              '/phidgets_daq/right_amp', 
              '/phidgets_daq/panels_xpos', 
              '/phidgets_daq/odor_pulse', 
              '/phidgets_daq/wba_left_m_right', 
              '/phidgets_daq/wba_left_p_right',
              '/ledpanels/pattern',
              '/ledpanels/command',
              ]
    directory = '~/Documents/panels_experiments/data'
    
    #LEDArena.start_rosbag_recording(topics, directory)
    
    while number_of_trials_done < number_of_trials:
        # strip fixation
        
        pattern_id = 5
        LEDArena.publish_to_led_panels.publish(command='set_pattern_id', arg1=pattern_id)
        rospy.sleep(.1)
        LEDArena.publish_to_led_panels.publish(command='start')
        print 'stripe fixation'
        rospy.sleep(stripe_fixation_length)
        LEDArena.publish_to_led_panels.publish(command='stop')
        
        #
        
        # pattern, with or without odor
        #ssr_val = np.random.randint(0,2)
        #publish_to_daq_ssr.publish([0], [ssr_val])
        
        pattern_id, pattern_name = choose_random_pattern(patterns_directory)
        LEDArena.publish_to_led_panels.publish(command='set_pattern_id', arg1=pattern_id)
        rospy.sleep(.1)
        LEDArena.publish_to_led_panels.publish(command='start')
        print pattern_id, ' : ', pattern_name
        rospy.sleep(trial_length)
        LEDArena.publish_to_led_panels.publish(command='stop')
        
        number_of_trials_done += 1
        
    #LEDArena.stop_rosbag_recording()
    
    
    
    
    

