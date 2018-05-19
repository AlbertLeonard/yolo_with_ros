cmake_minimum_required(VERSION 2.8.3)
project(joystick_controller)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs sensor_msgs 
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS node/joystick_controller.py
                 node/joystick_controller_btp.py
                 node/central_command.py
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
