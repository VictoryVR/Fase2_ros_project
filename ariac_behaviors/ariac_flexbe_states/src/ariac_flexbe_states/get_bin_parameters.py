#!/usr/bin/env python

import rospy
import xml.etree.ElementTree as ET
from flexbe_core import EventState, Logger


'''
Created on 10.10.2016

@author: Gerard Harkema
'''

class GetBinParameters(EventState):
        '''
	Finds the a camera near a bin en the robot configuration.

        ># bin          	string      Name of the bin.



	#> camera_topic		string	   Topic of the camera near the bin 
	#> camera_frame		string	   Frame of teh camera

	#> robot_config		string	   Robot configuration for the bin

        <= found                           Configuration for bin found.
        <= not_found                       No confuguration for the bin found

        '''

        def __init__(self):
                '''
                Constructor
                '''
                super(GetBinParameters, self).__init__(outcomes=['found', 'not_found'],
							input_keys = ['bin'],
                                                        output_keys=['camera_topic', 'camera_frame', 'robot_config'])


		self._param_error = False
		self._config = None


        def execute(self, userdata):
		if self._param_error :
			return 'not_found'
		return 'found'





        def on_enter(self, userdata):

                self._success         = False

                self._config_param = None
                if rospy.has_param('/ariac_config'):
                        self._config_param = rospy.get_param('/ariac_config')
                else:
                        Logger.logerr('Unable to get parameters: %s' % srdf_param)
	                self._param_error     = True
			return

                self._config = None


                try:
                        self._config = ET.fromstring(self._config_param)
                except Exception as e:
                        Logger.logwarn('Unable to parse given SRDF parameter: /ariac_config')
                        self._param_error = True
			return
		userdata.camera_topic = None
		userdata.camera_frame = None
		userdata.robot_config = None
                if not self._param_error:
	                for config in self._config.iter('config'):
		                for bin in config.iter('bin'):
		                        if userdata.bin == bin.attrib['name']:
						camera_config = None
						for camera_config in bin.iter('camera_topic') :
							userdata.camera_topic = camera_config.attrib['value']
							#Logger.logwarn(userdata.camera_topic)
						camera_frame = None
						for camera_frame in bin.iter('camera_frame') :
							userdata.camera_frame = camera_frame.attrib['value']
							#Logger.logwarn(userdata.camera_frame)						
						robot_config = None
						for robot_config in bin.iter('robot_config') :
							userdata.robot_config = robot_config.attrib['value']
							#Logger.logwarn(userdata.robot_config)						
                        if userdata.camera_topic is None or userdata.camera_frame is None or userdata.robot_config is None:
                                Logger.logwarn('Did not found items')
			        self._param_error     = True
				return

        def on_stop(self):
		pass

        def on_pause(self):
                pass

        def on_resume(self, userdata):
               pass
