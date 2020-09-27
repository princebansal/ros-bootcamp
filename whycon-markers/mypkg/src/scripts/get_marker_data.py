#!/usr/bin/env python

import rospy
import roslib
import tf

from geometry_msgs.msg import PoseArray


def callback(received_data):
	markerData = {}
	poses = received_data.poses
	for i, val in enumerate(poses):
		position = val.position
    	markerData[i] = [position.x, position.y, position.z]
    rospy.loginfo(markerData)
	rospy.loginfo("\n")


def Whycon_detect(): 
    rospy.init_node('whycon_detection', anonymous = True)
    rospy.Subscriber('/whycon/poses', PoseArray, callback)
    rospy.spin()

if __name__=="__main__":
	Whycon_detect()
    rospy.sleep(1)
