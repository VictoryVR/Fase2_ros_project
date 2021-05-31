#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.message_state import MessageState
from unit_2_flexbe_behaviors.pick_part_from_conveyor_sm import pick_part_from_conveyorSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_conveyor_testSM(Behavior):
	'''
	testbench to test the pick_part_from_ conveyor behavior
	'''


	def __init__(self):
		super(pick_part_from_conveyor_testSM, self).__init__()
		self.name = 'pick_part_from_conveyor_test'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(pick_part_from_conveyorSM, 'pick_part_from_conveyor')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:649 y:56, x:174 y:207
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part = ''
		_state_machine.userdata.robot_namespace = '/ariac/arm1'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:113 y:43
			OperatableStateMachine.add('pick_part_from_conveyor',
										self.use_behavior(pick_part_from_conveyorSM, 'pick_part_from_conveyor'),
										transitions={'finished': 'PartMessage', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'robot_namespace': 'robot_namespace', 'part': 'part'})

			# x:385 y:51
			OperatableStateMachine.add('PartMessage',
										MessageState(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
