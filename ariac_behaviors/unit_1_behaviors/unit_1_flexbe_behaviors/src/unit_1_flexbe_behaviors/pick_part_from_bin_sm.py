#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.get_vacuum_gripper_status_state import GetVacuumGripperStatusState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_logistics_flexbe_states.text_to_float_state import TextToFloatState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_binSM(Behavior):
	'''
	pick's a specific part form a it's bin
	'''


	def __init__(self):
		super(pick_part_from_binSM, self).__init__()
		self.name = 'pick_part_from_bin'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:319 y:186, x:898 y:309
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part', 'robot_namespace', 'robot'])
		_state_machine.userdata.part = ''
		_state_machine.userdata.robot_namespace = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = '/ariac/arm1'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.config_name_out = ''
		_state_machine.userdata.move_group_out = ''
		_state_machine.userdata.robot_name_out = ''
		_state_machine.userdata.action_topic_out = ''
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.zero = 0
		_state_machine.userdata.robot1 = 1
		_state_machine.userdata.robot = ''
		_state_machine.userdata.camera_ref_frame = 'world'
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.part_height = 0.035
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.gripper1_service = '/ariac/arm1/gripper/control'
		_state_machine.userdata.gripper2_service = '/ariac/arm2/gripper/control'
		_state_machine.userdata.gripper1_status_topic = '/ariac/arm1/gripper/state'
		_state_machine.userdata.gripper2_status_topic = '/ariac/arm1/gripper/state'
		_state_machine.userdata.gripper_enabled = False
		_state_machine.userdata.gripper_attached = False
		_state_machine.userdata.true_var = True
		_state_machine.userdata.r1_home_config = 'robot1PreGraspBin6'
		_state_machine.userdata.r2_home_config = 'robot2PreGraspBin1'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]


		with _state_machine:
			# x:35 y:36
			OperatableStateMachine.add('GetPartLocation',
										GetMaterialLocationsState(),
										transitions={'continue': 'GetBinFromLocations'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part', 'material_locations': 'locations'})

			# x:1294 y:488
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveR1ToPick1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_height', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1557 y:425
			OperatableStateMachine.add('Conversion_1',
										TextToFloatState(),
										transitions={'done': 'ComputePick'},
										autonomy={'done': Autonomy.Off},
										remapping={'text_value': 'part_height', 'float_value': 'part_height'})

			# x:1570 y:60
			OperatableStateMachine.add('DetectCameraPart',
										DetectPartCameraAriacState(time_out=1),
										transitions={'continue': 'movePre', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:428 y:40
			OperatableStateMachine.add('Differ r1 from r2',
										EqualState(),
										transitions={'true': 'R1 Home', 'false': 'R2 Home'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'robot', 'value_b': 'robot1'})

			# x:1126 y:431
			OperatableStateMachine.add('Differ r1 from r2_2',
										EqualState(),
										transitions={'true': 'activate gripper1-1', 'false': 'activate gripper2-1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'robot', 'value_b': 'robot1'})

			# x:206 y:36
			OperatableStateMachine.add('GetBinFromLocations',
										GetItemFromListState(),
										transitions={'done': 'Differ r1 from r2', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'locations', 'index': 'zero', 'item': 'bin'})

			# x:1582 y:333
			OperatableStateMachine.add('GetPartheightTable',
										LookupFromTableState(parameter_name='/ariac_unit1_tables', table_name='partheight_config', index_title='part', column_title='part_height_param'),
										transitions={'found': 'Conversion_1', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'part', 'column_value': 'part_height'})

			# x:1082 y:18
			OperatableStateMachine.add('LookupCameraFrame',
										LookupFromTableState(parameter_name='/ariac_unit1_tables', table_name='robot_1_table', index_title='bin', column_title='camera_frame'),
										transitions={'found': 'LookupPreGrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:1089 y:94
			OperatableStateMachine.add('LookupCameraFrame_2',
										LookupFromTableState(parameter_name='/ariac_unit1_tables', table_name='robot_2_table', index_title='bin', column_title='camera_frame'),
										transitions={'found': 'LookupPreGrasp_2', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:885 y:30
			OperatableStateMachine.add('LookupCameraTopic',
										LookupFromTableState(parameter_name='/ariac_unit1_tables', table_name='robot_1_table', index_title='bin', column_title='camera_topic'),
										transitions={'found': 'LookupCameraFrame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:874 y:97
			OperatableStateMachine.add('LookupCameraTopic_2',
										LookupFromTableState(parameter_name='/ariac_unit1_tables', table_name='robot_2_table', index_title='bin', column_title='camera_topic'),
										transitions={'found': 'LookupCameraFrame_2', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:1287 y:21
			OperatableStateMachine.add('LookupPreGrasp',
										LookupFromTableState(parameter_name='/ariac_unit1_tables', table_name='robot_1_table', index_title='bin', column_title='robot_config'),
										transitions={'found': 'DetectCameraPart', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:1285 y:92
			OperatableStateMachine.add('LookupPreGrasp_2',
										LookupFromTableState(parameter_name='/ariac_unit1_tables', table_name='robot_2_table', index_title='bin', column_title='robot_config'),
										transitions={'found': 'DetectCameraPart', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:1156 y:591
			OperatableStateMachine.add('MoveR1ToPick1',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Differ r1 from r2_2', 'planning_failed': 'WaitRetry3', 'control_failed': 'WaitRetry3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1596 y:252
			OperatableStateMachine.add('MoveToBin',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GetPartheightTable', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:16 y:229
			OperatableStateMachine.add('MoveToBin_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:647 y:19
			OperatableStateMachine.add('R1 Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'LookupCameraTopic', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'r1_home_config', 'move_group': 'move_group', 'action_topic_namespace': 'robot_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:646 y:96
			OperatableStateMachine.add('R2 Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'LookupCameraTopic_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'r2_home_config', 'move_group': 'move_group', 'action_topic_namespace': 'robot_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:224 y:435
			OperatableStateMachine.add('WaitForGrip',
										WaitState(wait_time=1),
										transitions={'done': 'movePre_2'},
										autonomy={'done': Autonomy.Off})

			# x:1435 y:658
			OperatableStateMachine.add('WaitRetry3',
										WaitState(wait_time=1),
										transitions={'done': 'DetectCameraPart'},
										autonomy={'done': Autonomy.Off})

			# x:933 y:404
			OperatableStateMachine.add('activate gripper1-1',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'deactivate gripper1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper1_service'})

			# x:573 y:407
			OperatableStateMachine.add('activate gripper1-2',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'get gripper1 state', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper1_service'})

			# x:939 y:508
			OperatableStateMachine.add('activate gripper2-1',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'deactivate gripper2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper2_service'})

			# x:588 y:508
			OperatableStateMachine.add('activate gripper2-2',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'get gripper2 state', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper2_service'})

			# x:757 y:404
			OperatableStateMachine.add('deactivate gripper1',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'activate gripper1-2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper1_service'})

			# x:769 y:510
			OperatableStateMachine.add('deactivate gripper2',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'activate gripper2-2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper2_service'})

			# x:384 y:410
			OperatableStateMachine.add('get gripper1 state',
										GetVacuumGripperStatusState(),
										transitions={'continue': 'WaitForGrip', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'topic_name': 'gripper1_status_topic', 'enabled': 'gripper_enabled', 'attached': 'gripper_attached'})

			# x:398 y:504
			OperatableStateMachine.add('get gripper2 state',
										GetVacuumGripperStatusState(),
										transitions={'continue': 'WaitForGrip', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'topic_name': 'gripper2_status_topic', 'enabled': 'gripper_enabled', 'attached': 'gripper_attached'})

			# x:1617 y:169
			OperatableStateMachine.add('movePre',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveToBin', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'robot_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:56 y:340
			OperatableStateMachine.add('movePre_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveToBin_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'robot_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:38 y:501
			OperatableStateMachine.add('CheckState',
										EqualState(),
										transitions={'true': 'movePre_2', 'false': 'DetectCameraPart'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_attached', 'value_b': 'true_var'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
