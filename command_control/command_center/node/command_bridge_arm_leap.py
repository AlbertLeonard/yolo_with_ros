#!/usr/bin/env python

import rospy
import wx
import math
import time

from leap_motion.msg import leap
from leap_motion.msg import leapros
from leap_motion.msg import leap_ui
from msg_gateway.srv import MoveArm, MoveArmResponse

hand_flag = 0
hand_init = 0
hand_init_flag = 0
hand_init_x = 0
hand_init_y = 0
hand_init_z = 0

hand_diff_flag = 0
hand_diff_x = 0
hand_diff_y = 0
hand_diff_z = 0

class Frame(wx.Frame):
	
	def __init__(self):
		
		global hand_flag, hand_init
		
		image_size = (640, 480)
		
		wx.Frame.__init__(self, None, -1, 'MyFrame', pos=(-1,-1), 
						  style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX), size=image_size)
		
		self.panel = wx.Panel(self,-1)
		self.timer = wx.Timer(self.panel, -1)
		self.timer.Start(10)
		self.panel.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		
		self.panel.SetBackgroundColour(wx.RED)
		
		wx.StaticText(self.panel, -1, 'Hand_Pos:', pos=(10,12))
		wx.StaticText(self.panel, -1, 'Hand_PYR:', pos=(10,40))
		wx.StaticText(self.panel, -1, 'Hand_Num:', pos=(10,68))
		wx.StaticText(self.panel, -1, 'States:',   pos=(10,94))
		
		self.SetClientSize(image_size)
		self.posCtrl1 = wx.TextCtrl(self.panel, -1, "", pos=(100, 6), size=(200,28))
		self.posCtrl2 = wx.TextCtrl(self.panel, -1, "", pos=(100,34), size=(200,28))
		self.posCtrl3 = wx.TextCtrl(self.panel, -1, "", pos=(100,62), size=(200,28))
		self.posCtrl4 = wx.TextCtrl(self.panel, -1, "", pos=(100,90), size=(200,28))
		
		
	def OnTimer(self, event):
	
		global hand_flag, hand_init, leap_command
		
		self.posCtrl3.SetValue('%s'%(hand_num))
		
		if hand_num == 1:
		
			#print 'standing by'
			self.posCtrl1.SetValue("%3.5s, %3.5s, %3.5s"%(frame.palmpos.x, frame.palmpos.y, frame.palmpos.z))
			self.posCtrl2.SetValue("%3.5s, %3.5s, %3.5s"%(frame.ypr.x,     frame.ypr.y,     frame.ypr.z    ))
			
			leap_command.x = 0.4
			leap_command.y = 0
			leap_command.z = 0.45
			leap_command.pitch = 0
			leap_command.roll  = 0
			leap_command.yaw   = 0
			
			rad = math.hypot(frame.palmpos.x, frame.palmpos.z)
			
			self.panel.SetBackgroundColour(wx.BLUE)
			
			if hand_flag == 1:
				
				self.posCtrl4.SetValue('controlling')
				
				leap_command.x =  (0.4-frame.palmpos.z/1000)
				leap_command.y =  (   -frame.palmpos.x/1000)
				leap_command.z =  (0.2+frame.palmpos.y/2000)
				leap_command.pitch = 0#frame.direction.x
				leap_command.roll  = 0#frame.direction.z
				leap_command.yaw   = 0#frame.direction.y
				
				#print 'leap motion controlling'
				#print 'x:%f y:%f z:%f '% (0.4+frame.palmpos.z/1000, frame.palmpos.x/1000, 0.2+frame.palmpos.y/2000)
				#print 'r:%f y:%f p:%f '% (frame.ypr.x/90, frame.ypr.y/90, frame.ypr.z/90)
				#print 'x:%d y:%d z:%d '% (frame.palmpos.x, frame.palmpos.y, frame.palmpos.z)
				self.panel.SetBackgroundColour(wx.GREEN)
		
			else:
				
				self.posCtrl4.SetValue('detecting')
				
				if rad < 60:
					
					if hand_init < 20:
						
						hand_init = hand_init + 1
						self.posCtrl4.SetValue('tracking')
						
					else:
						
						hand_flag = 1
				
			
		else:
			
			hand_flag = 0
			hand_init = 0
			
			self.panel.SetBackgroundColour(wx.RED)
			#self.result = leap_move_arm(0.2, 0, 0.2, 0, 0, 0)
			
			leap_command.x = 0.2
			leap_command.y = 0
			leap_command.z = 0.2
			leap_command.pitch = 0
			leap_command.roll  = 0
			leap_command.yaw   = 0
			
			if hand_num == 2:
				
				self.posCtrl1.SetValue("%s "%('deadman'))
				self.posCtrl2.SetValue("%s "%('deadman'))
				self.posCtrl4.SetValue('resting')
				
			else:
				
				self.posCtrl1.SetValue("%s "%('lost'))
				self.posCtrl2.SetValue("%s "%('lost'))
				self.posCtrl4.SetValue('resting')
				
		x = leap_command.x
		y = leap_command.y
		z = leap_command.z
		pitch = leap_command.pitch
		roll = leap_command.roll
		yaw = leap_command.yaw
		
		self.result = leap_move_arm(x,y,z,pitch,roll,yaw)
		
class App(wx.App):
	
	def OnInit(self):
		
		self.wxframe = Frame()
		self.wxframe.Centre()
		self.wxframe.Show()
		self.SetTopWindow(self.wxframe)
		
		return True
		
def callback_data(data):
	
	global frame
	
	frame = data
	#print 'r:%f y:%f p:%f '% (frame.ypr.x, frame.ypr.y, frame.ypr.z)
	#print 'r:%f y:%f p:%f '% (frame.direction.x, frame.direction.y, frame.direction.z)
	print 'x:%d y:%d z:%d '% (frame.palmpos.x, frame.palmpos.y, frame.palmpos.z)
	
	
def callback_ui(msg_ui):
	
	global hand_num
	
	hand_num = msg_ui.hand_num
	#print hand_num
	
	
#Main 
rospy.init_node('leap_motion_arm_control')

frame = leapros()
hand_num = leap_ui()
leap_command = MoveArm()

sub_data = rospy.Subscriber('/leapmotion/data', leapros, callback_data)
sub_ui   = rospy.Subscriber('/leapmotion/ui',   leap_ui, callback_ui)

rospy.wait_for_service('move_arm')

leap_move_arm = rospy.ServiceProxy('move_arm', MoveArm)

#texture_flag = texture_recognize()

while not rospy.is_shutdown():
	
	app = App()
	app.MainLoop()
	
