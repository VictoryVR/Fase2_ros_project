#!/bin/bash

# ROS tools
echo "Installing ROS Tools"
sudo apt update
sudo apt -y install python-catkin-tools \
		ros-melodic-moveit \
		joint-state-publisher \
		ros-melodic-joint-state-publisher-gui \
		ros-melodic-ros-control \
		ros-melodic-ros-controllers \
		gazebo9-plugin-base \
		libsdformat6 \
		libsdl-image1.2-dev \
		libnlopt-dev \
		ros-melodic-flexbe-behavior-engine \

#sudo apt upgrade libignition-math4

DOWNLOAD_DIRECTORY=../downloads
PACKAGE_DIRECTORY=../src/rospackages

# FlexBE-app
echo "Installing Flexbe"
DIRECTORY=$PACKAGE_DIRECTORY/flexbe_app
if [ ! -d  "$DIRECTORY" ]; then
	git clone https://github.com/FlexBE/flexbe_app.git $PACKAGE_DIRECTORY/flexbe_app
fi

#rm -r $DOWNLOAD_DIRECTORY
echo "Done installing"
