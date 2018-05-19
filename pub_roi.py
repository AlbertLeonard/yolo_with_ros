#!/usr/bin/env python
#!coding=utf-8

#modified by lyk at 2018.05.07

import rospy
import sys
from sensor_msgs.msg import Image, RegionOfInterest


def get_depth():
    #init ros_node
    rospy.init_node('roi_puber', anonymous=True)

    roi_pub = rospy.Publisher('/yolo_roi', RegionOfInterest, queue_size=2)
    rate = rospy.Rate(5) # 5hz

    #x,y(up_left),w,h
    roi_box=[320,240,30,20]
    while not rospy.is_shutdown():
        try:
            print '* trying *'
            ROI = RegionOfInterest()
            ROI.x_offset = int(roi_box[0])
            ROI.y_offset = int(roi_box[1])
            ROI.width = int(roi_box[2])
            ROI.height = int(roi_box[3])
            roi_pub.publish(ROI)
        except:
            rospy.loginfo("Publishing ROI failed")

        rate.sleep()


if __name__ == '__main__':
    get_depth()
