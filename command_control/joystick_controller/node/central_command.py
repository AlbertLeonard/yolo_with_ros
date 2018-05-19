#!/usr/bin/env python

import rospy 
import std_msgs 

from msg_gateway.msg import Command_msgs

frame = 0
mode = 0
function = 0
i = 0

def differ(now, pre ): #Generate UI_msg
	
	global mode, function
	
	if (now.Y - pre.Y) == 1:
		
		if mode < 3: #3 Modes in Total
			#print 'a'
			mode = mode + 1
		else:
			#print 'b'
			mode = 0
	if (now.SELECT - pre.SELECT) == 1:
		
		if function < 1: #3 Modes in Total
			function = function + 1
		else:
			function = 0
		
	

def callback(msg):

	global frame, i, MSG_pre 
	
	if i == 0:
		MSG_pre.X_ = 0 
		MSG_pre.A_ = 0 
		MSG_pre.B_ = 0 
		MSG_pre.Y_ = 0 
		MSG_pre.LB_ = 0 
		MSG_pre.RB_ = 0 
		MSG_pre.LT_ = 0 
		MSG_pre.RT_ = 0 
		MSG_pre.SELECT_  = 0 
		MSG_pre.START_  = 0 
		MSG_pre.L_ = 0 
		MSG_pre.R_ = 0 
		print "Central_Command Node Running ... "
		i = 1
	
	differ(msg, MSG_pre )
	
	
	
	#print '........'
	#print MSG_pre.X_, MSG_pre.A_, MSG_pre.B_, MSG_pre.Y_
	#print msg.X_, msg.A_, msg.B_, msg.Y_
	
	#print 'Mode: %d'%mode
	#print 'Function: %d'%function
	#print 'i = %d'%i
	#frame = frame + 1
	#print '%d'%frame
	
	MSG_pre = msg
	
	
#Main 
rospy.init_node('command_control')

#MSG = Command_msgs()
MSG_pre = Command_msgs()

sub = rospy.Subscriber('command_control', Command_msgs, callback )
#pub = rospy.Publisher('command_control/raw', Command_msgs, queue_size=10 )

rospy.spin()

