#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.add_offset_to_pose_state import AddOffsetToPoseState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
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
		# x:1482 y:482, x:623 y:376
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'ProductPose'])
		_state_machine.userdata.ProductPose = []
		_state_machine.userdata.part = ''
		_state_machine.userdata.offset = 0.05
		_state_machine.userdata.part_rotation = ''
		_state_machine.userdata.robot_config1 = 'robot1AGV'
		_state_machine.userdata.robot_config2 = 'robot2AGV'
		_state_machine.userdata.robot1_namespace = '/ariac/arm1'
		_state_machine.userdata.robot2_namespace = '/ariac/arm2'
		_state_machine.userdata.gripper1_service = 'ariac/arm1/gripper/control'
		_state_machine.userdata.gripper2_service = 'ariac/arm2/gripper/control'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.frame_agv1 = 'kit_tray_1'
		_state_machine.userdata.frame_agv2 = 'kit_tray_2'
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.agv1 = 'agv1'
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.ProductType = ''
		_state_machine.userdata.offset_pose = 0.1
		_state_machine.userdata.ref_frame_th = 'arm1_linear_arm_actuator'
		_state_machine.userdata.zero = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]


		with _state_machine:
			# x:64 y:233
			OperatableStateMachine.add('equal',
										EqualState(),
										transitions={'true': 'preMove', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv1'})

			# x:653 y:30
			OperatableStateMachine.add('Message',
										MessageState(),
										transitions={'continue': 'addOffset'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ProductPose'})

			# x:796 y:29
			OperatableStateMachine.add('addOffset',
										AddOffsetToPoseState(),
										transitions={'continue': 'calcPlacePosAGV1'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'agv_pose', 'offset_pose': 'ProductPose', 'output_pose': 'agv_pose'})

			# x:968 y:31
			OperatableStateMachine.add('calcPlacePosAGV1',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'placeOnAGV1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'robot1_namespace', 'tool_link': 'tool_link', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'zero', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1357 y:52
			OperatableStateMachine.add('deactivate gripper1',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'finished', 'failed': 'deactivate gripper1'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper1_service'})

			# x:1159 y:31
			OperatableStateMachine.add('placeOnAGV1',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'deactivate gripper1', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot1_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:307 y:30
			OperatableStateMachine.add('preMove',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPose', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config1', 'move_group': 'move_group', 'action_topic_namespace': 'robot1_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:488 y:28
			OperatableStateMachine.add('GetPose',
										GetObjectPoseState(),
										transitions={'continue': 'Message', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame_th', 'frame': 'frame_agv1', 'pose': 'agv_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
