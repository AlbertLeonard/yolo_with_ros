#!/usr/bin/env python

import rospy 
import std_msgs 

from sensor_msgs.msg import Joy 
from msg_gateway.msg import Command_msgs

#Variables 
i = 0 

#Mapping Joystick 
class Joystick:
	
	# Left Stick 
	LS_H = 0 
	LS_V = 0 
	
	# Right Stick 
	RS_H = 0 
	RS_V = 0 
	
	# Direction Panel 
	DP_H = 0 
	DP_V = 0 
	
	# Buttons 
	X = 0 
	A = 0 
	B = 0 
	Y = 0 
	LB = 0 
	RB = 0 
	LT = 0 
	RT = 0 
	SELECT  = 0 
	START  = 0 
	L = 0 
	R = 0 
	
	# Buttons_Toggle_Buff 
	X_ = 0 
	A_ = 0 
	B_ = 0 
	Y_ = 0 
	LB_ = 0 
	RB_ = 0 
	LT_ = 0 
	RT_ = 0 
	SELECT_  = 0 
	START_  = 0 
	L_ = 0 
	R_ = 0 
	
	def __init__(self, joy_msg ):
	
		# Left Stick 
		self.LS_H = joy_msg.axes[0] 
		self.LS_V = joy_msg.axes[1] 
	
		# Right Stick 
		self.RS_H = joy_msg.axes[2] 
		self.RS_V = joy_msg.axes[3] 
	
		# Direction Panel 
		self.DP_H = joy_msg.axes[6] 
		self.DP_V = joy_msg.axes[7] 
	
		# Buttons 
		self.X = joy_msg.buttons[3] 
		self.A = joy_msg.buttons[0] 
		self.B = joy_msg.buttons[1] 
		self.Y = joy_msg.buttons[4] 
	
		self.LB = joy_msg.buttons[6] 
		self.RB = joy_msg.buttons[7] 
	
		self.LT = joy_msg.buttons[8] 
		self.RT = joy_msg.buttons[9] 
	
		self.SELECT  = joy_msg.buttons[10] 
		self.START  = joy_msg.buttons[11] 
	
		self.L = joy_msg.buttons[13] 
		self.R = joy_msg.buttons[14] 

	def switch(self, n):
		
		if n == 0:
			return 1
		else:
			return 0
	
	

def prepare_data(out, come, raw ):
	
	out.LS_H = raw.axes[0]
	out.LS_V = raw.axes[1]
	out.RS_H = raw.axes[2]
	out.RS_V = raw.axes[3]
	out.DP_H = raw.axes[6]
	out.DP_V = raw.axes[7]
	
	out.X = come.X
	out.A = come.A
	out.B = come.B
	out.Y = come.Y
	out.LB = come.LB
	out.RB = come.RB
	out.LT = come.LT
	out.RT = come.RT
	out.SELECT = come.SELECT
	out.START = come.START
	out.L = come.L
	out.R = come.R
	
	out.X_ = come.X_
	out.A_ = come.A_
	out.B_ = come.B_
	out.Y_ = come.Y_
	out.LB_ = come.LB_
	out.RB_ = come.RB_
	out.LT_ = come.LT_
	out.RT_ = come.RT_
	out.SELECT_ = come.SELECT_
	out.START_ = come.START_
	out.L_ = come.L_
	out.R_ = come.R_
	
	return out
	
	
def press_detect(now, pre ):
	
	if (now.X - pre.X ) == 1: 
		now.X_ = now.switch(now.X_) 
	if (now.A - pre.A ) == 1: 
		now.A_ = now.switch(now.A_) 
	if (now.B - pre.B ) == 1: 
		now.B_ = now.switch(now.B_) 
	if (now.Y - pre.Y ) == 1: 
		now.Y_ = now.switch(now.Y_) 
	if (now.LB - pre.LB ) == 1: 
		now.LB_ = now.switch(now.LB_) 
	if (now.RB - pre.RB ) == 1: 
		now.RB_ = now.switch(now.RB_) 
	if (now.LT - pre.LT ) == 1: 
		now.LT_ = now.switch(now.LT_) 
	if (now.RT - pre.RT ) == 1: 
		now.RT_ = now.switch(now.RT_) 
	if (now.SELECT - pre.SELECT ) == 1: 
		now.SELECT_ = now.switch(now.SELECT_) 
	if (now.START - pre.START ) == 1: 
		now.START_ = now.switch(now.START_) 
	if (now.L - pre.L ) == 1: 
		now.L_ = now.switch(now.L_) 
	if (now.R - pre.R ) == 1: 
		now.R_ = now.switch(now.R_) 
		
	
#Simple Time Filter 
def differ(now, pre ):

	pre.X = now.X 
	pre.A = now.A 
	pre.B = now.B 
	pre.Y = now.Y 
	pre.LB = now.LB 
	pre.RB = now.RB 
	pre.LT = now.LT 
	pre.RT = now.RT 
	pre.SELECT = now.SELECT 
	pre.START = now.START 
	pre.L = now.L 
	pre.R = now.R 
	
	pre.X_ = now.X_ 
	pre.A_ = now.A_ 
	pre.B_ = now.B_ 
	pre.Y_ = now.Y_ 
	pre.LB_ = now.LB_ 
	pre.RB_ = now.RB_ 
	pre.LT_ = now.LT_ 
	pre.RT_ = now.RT_ 
	pre.SELECT_ = now.SELECT_ 
	pre.START_ = now.START_ 
	pre.L_ = now.L_ 
	pre.R_ = now.R_ 
	
#Update Joystick Msgs 
def update_joystick(joy_msg):

	global MSG_pre 
	MSG = Joystick(joy_msg) 
	
	
	#print '----- ' 
	#print i 
	#print MSG_pre.X, MSG_pre.A, MSG_pre.B, MSG_pre.Y 
	#print MSG.X, MSG.A, MSG.B, MSG.Y 
	#print MSG.X_, MSG.A_, MSG.B_, MSG.Y_ 
	
	press_detect(MSG, MSG_pre )
	
	#filter
	differ(MSG, MSG_pre) 
	
	#print toggle_buff.X_, toggle_buff.A_, toggle_buff.B_, toggle_buff.Y_ 
	#print Joystick.X, Joystick.A, Joystick.B, Joystick.Y 
	
	
def callback(msg):
	
	global i, OUT 
	
	if i == 0:
		MSG_pre.X = 0 
		MSG_pre.A = 0 
		MSG_pre.B = 0 
		MSG_pre.Y = 0 
		MSG_pre.LB = 0 
		MSG_pre.RB = 0 
		MSG_pre.LT = 0 
		MSG_pre.RT = 0 
		MSG_pre.SELECT  = 0 
		MSG_pre.START  = 0 
		MSG_pre.L = 0 
		MSG_pre.R = 0 
		print "Joystick Remapping Node Running ..."
		i = 1
	
	update_joystick(msg)
	OUT = prepare_data(OUT, MSG, msg)
	
	
	
#Main Part
rospy.init_node('joystick_controller')

MSG_pre = Joystick
MSG = Joystick
OUT = Command_msgs()

rate = rospy.Rate(30) # 30hz

sub = rospy.Subscriber('/command_control/raw', Joy, callback )
pub = rospy.Publisher('command_control', Command_msgs, queue_size=1 )

while not rospy.is_shutdown():

	pub.publish(OUT)
	rate.sleep()
	
