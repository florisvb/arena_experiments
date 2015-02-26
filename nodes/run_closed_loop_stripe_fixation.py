#!/usr/bin/env python
import rospy
import arena_experiments
import numpy as np
import time
import os


if __name__ == '__main__':
    rospy.init_node('experiment_controller')
    
    LEDArena = arena_experiments.LEDArena()
    
    LEDArena.run_closed_loop_pattern(5, ypos=0, pattern_name='stripe')
    
    
    
    
    

