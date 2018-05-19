#!/usr/bin/env python

import rospy
import std_msgs

from geometry_msgs.msg import Twist
from msg_gateway.msg import Command_msgs

def callback(msg):

	global GO, STOP 
	
	MSG_pre = msg
	
	if msg.START_ == 0:
	
		if (msg.LT == 1 ) and (msg.RT == 1 ):
		
			# Warning! WARNING!
		
			# Safe Speed Max: Linear 0.1, Angular 0.25 
		
			GO.linear.x = 0 * msg.LS_V # Base Forward-Backward
			GO.linear.y = 0 * msg.LS_H # Base Left_Cutl-Right_Cut
			GO.linear.z = 0 * (msg.R - msg.L ) # Lifter Up-Down
		
			GO.angular.x = 0 * msg.RS_H # Head Turn Left-Right #Roll Currently Not in Use
			GO.angular.y = 0 * msg.RS_V # Head Up-Down #Yaw
			GO.angular.z = 0 * (msg.LB - msg.RB ) #Base Turn Left-Right #Pitch	
		
		else:
	
			if msg.SELECT_ == 1:
		
				GO.linear.x = 0.1 * msg.LS_V # Base Forward-Backward
				GO.linear.y = 0.1 * msg.LS_H # Base Left_Cutl-Right_Cut
				GO.linear.z = 0.1 * (msg.R - msg.L ) # Lifter Up-Down
		
				GO.angular.x = 0.1 * msg.RS_H # Head Turn Left-Right #Roll Currently Not in Use
				GO.angular.y = 0.1 * msg.RS_V # Head Up-Down #Yaw
				GO.angular.z = 0.3 * (msg.LB - msg.RB ) #Base Turn Left-Right #Pitch
		
			else:
		
				GO.linear.x = 0.25 * msg.LS_V # Base Forward-Backward
				GO.linear.y = 0.25 * msg.LS_H # Base Left_Cutl-Right_Cut
				GO.linear.z = 0.25 * (msg.R - msg.L ) # Lifter Up-Down
		
				GO.angular.x = 0.25 * msg.RS_H # Head Turn Left-Right #Roll Currently Not in Use
				GO.angular.y = 0.25 * msg.RS_V # Head Up-Down #Yaw
				GO.angular.z = 0.6 * (msg.LB - msg.RB ) #Base Turn Left-Right #Pitch
		
		#GO.angular.x = 0 # Roll Currently Not in Use
		#GO.angular.y = msg.RS_V # Yaw
		#GO.angular.z = msg.RS_H # Pitch
		
	else:
		
		GO.linear.x = 0
		GO.linear.y = 0
		GO.linear.z = 0
		
		GO.angular.x = 0
		GO.angular.y = 0
		GO.angular.z = 0
		
	
	cmd_vel_pub.publish(GO)
	
	
#Main 
#cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1 )
cmd_vel_pub = rospy.Publisher('cmd_vel_mux', Twist, queue_size = 1 )

STOP = Twist()
GO = Twist()

rospy.init_node('command_bridge_base_joy')
	
sub_joy = rospy.Subscriber('command_control', Command_msgs, callback)

#pub = rospy.Publisher('command_control/raw', Command_msgs, queue_size=10 )

rospy.loginfo("Command_Bridge_Base_Joy...")

rospy.spin()

