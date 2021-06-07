#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_example_behaviors.get_order_sm import get_orderSM
from unit_1_flexbe_behaviors.pick_part_from_bin_sm import pick_part_from_binSM
from unit_1_flexbe_behaviors.unit1_agv_place_move_sm import unit1_AGV_place_moveSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_bin_testSM(Behavior):
	'''
	testbench to test the pick_part_from_bin behavior
	'''


	def __init__(self):
		super(pick_part_from_bin_testSM, self).__init__()
		self.name = 'pick_part_from_bin_test'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(pick_part_from_binSM, 'PickPartFromBin')
		self.add_behavior(get_orderSM, 'get_order')
		self.add_behavior(unit1_AGV_place_moveSM, 'unit1_AGV_place_move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:860 y:346, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part = 'gasket_part'
		_state_machine.userdata.robot_namespace = '/ariac/arm1'
		_state_machine.userdata.robot = 1
		_state_machine.userdata.agv_id = 'agv1'
		_state_machine.userdata.ProductPose = []
		_state_machine.userdata.ProductType = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]


		with _state_machine:
			# x:135 y:72
			OperatableStateMachine.add('PickPartFromBin',
										self.use_behavior(pick_part_from_binSM, 'PickPartFromBin'),
										transitions={'finished': 'get_order', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'part', 'robot_namespace': 'robot_namespace', 'robot': 'robot'})

			# x:337 y:114
			OperatableStateMachine.add('get_order',
										self.use_behavior(get_orderSM, 'get_order'),
										transitions={'finished': 'unit1_AGV_place_move', 'fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'fail': Autonomy.Inherit},
										remapping={'ProductType': 'ProductType', 'ProductPose': 'ProductPose'})

			# x:584 y:179
			OperatableStateMachine.add('unit1_AGV_place_move',
										self.use_behavior(unit1_AGV_place_moveSM, 'unit1_AGV_place_move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'ProductPose': 'ProductPose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
