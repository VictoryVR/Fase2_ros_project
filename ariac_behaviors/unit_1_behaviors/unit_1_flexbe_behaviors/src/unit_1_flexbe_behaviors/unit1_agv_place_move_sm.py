#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 02 2021
@author: Victor Verschuur
'''
class unit1_AGV_place_moveSM(Behavior):
	'''
	the placing of parts and the moving of the AGV
	'''


	def __init__(self):
		super(unit1_AGV_place_moveSM, self).__init__()
		self.name = 'unit1_AGV_place_move'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id'])
		_state_machine.userdata.list = []
		_state_machine.userdata.part = ''
		_state_machine.userdata.robot_namespace = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = '/ariac/arm1'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.camera_ref_frame = 'world'
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.gripper2_service = '/ariac/arm2/gripper/control'
		_state_machine.userdata.gripper1_status_topic = 'ariac/arm1/gripper/status'
		_state_machine.userdata.part_height = 0
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.gripper1_service = '/ariac/arm1/gripper/control'
		_state_machine.userdata.gripper2_status_topic = 'ariac/arm2/gripper/status'
		_state_machine.userdata.robot = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.agv1 = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:137 y:53
			OperatableStateMachine.add('equal',
										EqualState(),
										transitions={'true': 'finished', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv1'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
