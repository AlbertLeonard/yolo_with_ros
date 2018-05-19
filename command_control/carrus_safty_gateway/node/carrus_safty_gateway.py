#!/usr/bin/env python
# 2016-05-01
# Dee

import rospy
import std_msgs

from geometry_msgs.msg import Twist
from msg_gateway.msg import Command_msgs

class velocityGateway:
	
	def __init__(self):
		
		self.FILTER_CONST_LAST = 0.9
		self.FILTER_CONST_NOW  = 1 - self.FILTER_CONST_LAST
		
		self.BUFF_LEN = 10
		self.DEADMAN = False
		self.NAVIGATION_IS_ON = True
		self.JOY_IS_ON = False
		self.MODE = 0        # 0:Normal-Speed 
							 # 1:Low-Speed
		                     # TODO:Multiplexer
		
		self.CONST_LINEAR_X = 0
		self.CONST_LINEAR_Y = 0
		self.CONST_LINEAR_Z = 0
		self.CONST_ANGULAR_X = 0
		self.CONST_ANGULAR_Y = 0
		self.CONST_ANGULAR_Z = 0
		
		
		self.velocity_mux_nav          = Twist()
		self.velocity_mux_final        = Twist()
		self.velocity_mux_now          = Twist()
		self.velocity_mux_last         = Twist()
		self.velocity_mux_temp         = Twist()
		self.velocity_mux_filtered     = [self.velocity_mux_temp] * self.BUFF_LEN
		
		self.velocity_mux_pub = rospy.Publisher('cmd_vel_mux', Twist, queue_size = 1) #/input/teleop
		self.velocity_mux_joy_pub = rospy.Publisher('cmd_vel_mux_joy', Twist, queue_size = 1)
		
		rospy.loginfo("Carrus base safty gateway initializing...")
		
	def check(self, msg):
		
		# Checking Joy for Joy Priority
		
		if (msg.LS_H == 0) and (msg.LS_V == 0) and (msg.RS_H == 0) and (msg.RS_V == 0) and (msg.DP_H == 0) and (msg.DP_V == 0) and (msg.X == 0)    and (msg.A == 0) and (msg.B == 0) and (msg.Y == 0) and (msg.LB == 0) and (msg.RB == 0) and (msg.LT == 0) and (msg.RT == 0) and (msg.SELECT == 0) and (msg.START == 0) and (msg.L == 0) and (msg.R == 0):
		   
			self.JOY_IS_ON = False
			#self.NAVIGATION_IS_ON = True
			
		else:
			
			self.JOY_IS_ON = True
			self.NAVIGATION_IS_ON = False
		
		
		# Warning! WARNING!
		# Safe Speed Const Max: Linear 0.3, Angular 0.60 at 30Hz
		
		if (msg.LT == 1 ) and (msg.RT == 1 ):
			
			self.DEADMAN = True
			
			self.CONST_LINEAR_X = 0
			self.CONST_LINEAR_Y = 0
			self.CONST_LINEAR_Z = 0
			self.CONST_ANGULAR_X = 0
			self.CONST_ANGULAR_Y = 0
			self.CONST_ANGULAR_Z = 0
			
		else:
			
			self.DEADMAN = False
			
			if msg.SELECT_ == 1:
				
				self.MODE = 1
				
				self.CONST_LINEAR_X = 0.1
				self.CONST_LINEAR_Y = 0.1
				self.CONST_LINEAR_Z = 0.1
				self.CONST_ANGULAR_X = 0.1
				self.CONST_ANGULAR_Y = 0.1
				self.CONST_ANGULAR_Z = 0.3
				
			else:
				
				self.MODE = 0
				
				self.CONST_LINEAR_X = 0.3
				self.CONST_LINEAR_Y = 0.3
				self.CONST_LINEAR_Z = 0.3
				self.CONST_ANGULAR_X = 0.3
				self.CONST_ANGULAR_Y = 0.3
				self.CONST_ANGULAR_Z = 0.6
				
		#TODO: More safty measure to be added
			
	def velocity_filter(self, vel_msg):
		
		# Simple Python list for speed smoothing
		
		self.velocity_mux_now = vel_msg
		
		# Smoothing
		
		self.velocity_mux_temp.linear.x = self.FILTER_CONST_NOW * self.velocity_mux_now.linear.x + self.FILTER_CONST_LAST * self.velocity_mux_filtered[0].linear.x
		self.velocity_mux_temp.linear.y = self.FILTER_CONST_NOW * self.velocity_mux_now.linear.y + self.FILTER_CONST_LAST * self.velocity_mux_filtered[0].linear.y
		self.velocity_mux_temp.linear.z = self.FILTER_CONST_NOW * self.velocity_mux_now.linear.z + self.FILTER_CONST_LAST * self.velocity_mux_filtered[0].linear.z
		
		self.velocity_mux_temp.angular.x = self.FILTER_CONST_NOW * self.velocity_mux_now.angular.x + self.FILTER_CONST_LAST * self.velocity_mux_filtered[0].angular.x
		self.velocity_mux_temp.angular.y = self.FILTER_CONST_NOW * self.velocity_mux_now.angular.y + self.FILTER_CONST_LAST * self.velocity_mux_filtered[0].angular.y
		self.velocity_mux_temp.angular.z = self.FILTER_CONST_NOW * self.velocity_mux_now.angular.z + self.FILTER_CONST_LAST * self.velocity_mux_filtered[0].angular.z
		
		# Deadzone Check
		
		self.velocity_mux_temp.linear.x  = self.velocity_deadzone(self.velocity_mux_temp.linear.x)
		self.velocity_mux_temp.linear.y  = self.velocity_deadzone(self.velocity_mux_temp.linear.y)
		self.velocity_mux_temp.linear.z  = self.velocity_deadzone(self.velocity_mux_temp.linear.z)
		self.velocity_mux_temp.angular.x = self.velocity_deadzone(self.velocity_mux_temp.angular.x)
		self.velocity_mux_temp.angular.y = self.velocity_deadzone(self.velocity_mux_temp.angular.y)
		self.velocity_mux_temp.angular.z = self.velocity_deadzone(self.velocity_mux_temp.angular.z)
		
		# Quene
		
		self.velocity_mux_filtered.append(self.velocity_mux_temp)
		self.velocity_mux_filtered.pop(0)
		
		self.velocity_mux_last = self.velocity_mux_now
		
	def velocity_deadzone(self, vel_in):
		
		if abs(vel_in) < 0.01:
			
			vel_out = 0
			
		else:
			
			vel_out = vel_in
			
		return vel_out
		
	# TODO: def velocity_multiplexer(self):
	
	def velocity_publisher(self):
		
		# Source select
		
		if (self.velocity_mux_filtered[self.BUFF_LEN-1].linear.x == 0) and (self.velocity_mux_filtered[self.BUFF_LEN-1].linear.y == 0) and (self.velocity_mux_filtered[self.BUFF_LEN-1].linear.z == 0) and (self.velocity_mux_filtered[self.BUFF_LEN-1].angular.x == 0) and (self.velocity_mux_filtered[self.BUFF_LEN-1].angular.y == 0) and (self.velocity_mux_filtered[self.BUFF_LEN-1].angular.z == 0):
			
			if (self.velocity_mux_nav.linear.x == 0) and (self.velocity_mux_nav.linear.y == 0) and (self.velocity_mux_nav.linear.z == 0) and (self.velocity_mux_nav.angular.x == 0) and (self.velocity_mux_nav.angular.y == 0) and (self.velocity_mux_nav.angular.z == 0):
				
				pass
				
			else:
			
				self.velocity_mux_final = self.velocity_mux_nav
				
				self.velocity_mux_pub.publish(self.velocity_mux_final)
				
				#print 'nav_on'
			
		else:
			
			#if self.JOY_IS_ON:
				
			self.velocity_mux_final = self.velocity_mux_filtered[self.BUFF_LEN-1]
				
			self.velocity_mux_pub.publish(self.velocity_mux_final)
			
			#print 'zero_on'
				
		# Publish with Multiplexer
		# pub /cmd_mux_joy for DEBUG
		self.velocity_mux_joy_pub.publish(self.velocity_mux_filtered[self.BUFF_LEN-1])
		
		
	def joy_callback(self, msg):
		
		self.check(msg)
		
		if not self.DEADMAN == True:
			
			# Calculate from joy input
			
			self.velocity_mux_now.linear.x  = self.CONST_LINEAR_X  *  msg.LS_V               # Base Forward-Backward
			self.velocity_mux_now.linear.y  = self.CONST_LINEAR_Y  *  msg.LS_H               # Base Left_Cutl-Right_Cut
			self.velocity_mux_now.linear.z  = self.CONST_LINEAR_Z  * (msg.R - msg.L )        # Lifter Up-Down
			
			self.velocity_mux_now.angular.x = self.CONST_ANGULAR_X *  msg.RS_H               # Head Turn Left-Right #Roll Currently Not in Use
			self.velocity_mux_now.angular.y = self.CONST_ANGULAR_Y *  msg.RS_V               # Head Up-Down #Yaw
			self.velocity_mux_now.angular.z = self.CONST_ANGULAR_Z * (msg.LB - msg.RB )      # Base Turn Left-Right #Pitch	
			
			self.velocity_filter(self.velocity_mux_now)
			
			self.velocity_publisher()
			
		else:
			
			# Enforced zero velocity output for double insurance
			# May be redundant ...
			
			self.velocity_mux_now.linear.x = 0
			self.velocity_mux_now.linear.y = 0
			self.velocity_mux_now.linear.z = 0
		
			self.velocity_mux_now.angular.x = 0
			self.velocity_mux_now.angular.y = 0
			self.velocity_mux_now.angular.z = 0
			
			self.velocity_mux_pub.publish(self.velocity_mux_now)
					
	def nav_callback(self, msg):
		
		# Publish rate is driven by joystick topic at 30hz
		
		self.velocity_mux_nav = msg
		
		#self.velocity_publisher()
		
#Main 
rospy.init_node('carrus_safty_gateway')

velocity_gateway = velocityGateway()

sub_joy = rospy.Subscriber('command_control', Command_msgs, velocity_gateway.joy_callback)
sub_nav = rospy.Subscriber('cmd_vel_mux_nav', Twist, velocity_gateway.nav_callback)

rospy.loginfo("Carrus base safty gateway initialized...")

rospy.spin()

