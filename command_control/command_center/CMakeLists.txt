cmake_minimum_required(VERSION 2.8.3)
project(command_center)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  sensor_msgs
  )


catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
  node/arm_auto_move.py
  node/command_bridge_base_joy.py
  node/command_bridge_base_leap.py
  node/command_bridge_arm_srv.py
  node/command_bridge_arm_joy.py
  node/command_bridge_arm_leap.py
  node/command_bridge_arm_voice.py
  
  node/robot_control_amanda.py
  
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
