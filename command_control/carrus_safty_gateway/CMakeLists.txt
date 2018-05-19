cmake_minimum_required(VERSION 2.8.3)
project(carrus_safty_gateway)

find_package(catkin REQUIRED COMPONENTS
  rospy
  tf
  std_msgs
  sensor_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS
  rospy
  std_msgs
  tf
  sensor_msgs
  geometry_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS node/carrus_safty_gateway.py
				 node/carrus_base_state.py

        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
