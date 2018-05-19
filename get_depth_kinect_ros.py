#!/usr/bin/env python
#!coding=utf-8

# modified by lyk at 2018.05.07
# CoordinateMapper
# https://www.jianshu.com/p/ec8deee8e137
# https://blog.csdn.net/hffhjh111/article/details/52503115
# https://blog.csdn.net/shihz_fy/article/details/43602393
# https://www.cnblogs.com/gaoxiang12/p/4652478.html

# https://stackoverflow.com/questions/13296059/kinect-converting-from-rgb-coordinates-to-depth-coordinates
# https://stackoverflow.com/questions/15936330/kinect-sdk-align-depth-and-color-frames

import rospy
import cv2
import sys
from sensor_msgs.msg import Image, RegionOfInterest
from cv_bridge import CvBridge, CvBridgeError
import math

def callback(img):
    #bridge=CvBridge()
    #cv_image = bridge.imgmsg_to_cv2(img, "32FC1")
    global x,y,f
    #d=cv_image[x,y]/1000
    '''
    print '**OK**'
    if x>0 and y>0:
        print cv_image[x,y]/1000, 'm'
    '''
    d = 0.832
    if (x>0 and y>0):
        xv = x-160
        yv = y-120
        zw = d*f/math.sqrt(f*f+xv**2+yv**2)
        xw = zw*xv/f
        yw = zw*yv/f
        print '---'
        print (xw,yw,zw)
        print ''

    else:
        print '... ...'
        print ''

def get_roi(msg):
    global x,y
    x=msg.x_offset/2+msg.width*1.0/2/2
    y=msg.y_offset/2+msg.height*1.0/2/2

def get_depth():
    #init ros_node
    rospy.init_node('get_depth_node', anonymous=True)
    global x,y,f
    x=140
    y=150
    rospy.Subscriber('webcam/image_raw', Image, callback)
    rospy.Subscriber('/yolo_roi', RegionOfInterest, get_roi)
    print '** Node init succeed ! **'
    f = 240.0/(2*math.tan(43.0/180*math.pi))
    print 'f=',f    #=

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    get_depth()
 



