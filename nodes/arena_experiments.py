#!/usr/bin/env python
from __future__ import division
import roslib
import rospy
import serial
import numpy as N
import subprocess, signal, os

from ledpanels.msg import MsgPanelsCommand
from ledpanels.srv import *

from std_msgs.msg import *    
    
class LEDArena:
    def __init__(self):
        self.publish_to_led_panels = rospy.Publisher('/ledpanels/command', MsgPanelsCommand, latch=True)
        self.publish_pattern_name = rospy.Publisher('/ledpanels/pattern', String, queue_size=3)
        rospy.sleep(2)
        try:
            rospy.init_node('led_arena_controller')
        except:
            pass
        self.publish_to_led_panels.publish(command='ctr_reset')
        rospy.sleep(5)
        self.publish_to_led_panels.publish(command='send_gain_bias', arg1=-10, arg2=0, arg3=0, arg4=0)
        rospy.sleep(1)
        self.publish_to_led_panels.publish(command='set_mode', arg1=1, arg2=0)
        rospy.sleep(1)
        
    def run_closed_loop_pattern(self, pattern_id, xgain=-10, ypos=0, pattern_name='pattern_name'):
        self.publish_to_led_panels.publish(command='stop')
        rospy.sleep(.1)
        self.publish_to_led_panels.publish(command='set_pattern_id', arg1=pattern_id)
        rospy.sleep(.1)
        self.publish_to_led_panels.publish(command='start')
        self.publish_pattern_name.publish(pattern_name)
        
    def start_rosbag_recording(self, topics, directory='~/'):
        directory = os.path.expanduser(directory)
        topics_with_spaces = [topic + ' ' for topic in topics]
        command = 'rosbag record ' + ''.join(topics_with_spaces)
        print 'rosbag record command: ', command
        self.rosbag_process_id = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True, cwd=directory)
        #self.rosbag_process_id = subprocess.Popen([command, "Subprocess"], preexec_fn=os.setsid)
        print 'recording bagfile for: ', topics
        print 'to directory: ', directory
        print 
        print 'pid: ', self.rosbag_process_id
        
    def stop_rosbag_recording(self):
        # kill process and children
        pid = self.rosbag_process_id.pid
        pgid = os.getpgid(pid)
        os.killpg(pgid, signal.SIGINT)
        print 'rosbag recording STOPPED'
