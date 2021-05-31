#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_example_behaviors.notify_shipment_ready_sm import notify_shipment_readySM
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.get_vacuum_gripper_status_state import GetVacuumGripperStatusState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Apr 16 2020
@author: Gerard Harkema
'''
class ariac_exampleSM(Behavior):
	'''
	Voorbeeld statemachine voor de ariac 2019 opdracht
	'''


	def __init__(self):
		super(ariac_exampleSM, self).__init__()
		self.name = 'ariac_example'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(notify_shipment_readySM, 'DeliverShipment')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:178 y:226, x:646 y:373
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.part = 'gasket_part'
		_state_machine.userdata.offset = 0.1
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = '/ariac/arm1'
		_state_machine.userdata.config_name_home = 'home'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.robot_config = ''
		_state_machine.userdata.config_name_tray1PreDrop = 'tray1PreDrop'
		_state_machine.userdata.camera_ref_frame = 'arm1_linear_arm_actuator'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.part_height = 0.035
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.conveyor_belt_power = 100.0
		_state_machine.userdata.arm_id = "arm1"
		_state_machine.userdata.part_drop_offset = 0.1
		_state_machine.userdata.tray = 'kit_tray_1'
		_state_machine.userdata.bin = ''
		_state_machine.userdata.locations = []
		_state_machine.userdata.zero = 0
		_state_machine.userdata.gripper_service = '/ariac/arm1/gripper/control'
		_state_machine.userdata.gripper_status_topic = '/ariac/arm1/gripper/state'
		_state_machine.userdata.gripper_status_attached = False
		_state_machine.userdata.gripper_status_enabled = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:20 y:140
			OperatableStateMachine.add('StartAssignment',
										StartAssignment(),
										transitions={'continue': 'SetConveyorbeltPower'},
										autonomy={'continue': Autonomy.Off})

			# x:1019 y:444
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveR1ToPick1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_height', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:17 y:506
			OperatableStateMachine.add('ComuteDorp',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveR1ToDrop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'agv_pose', 'offset': 'part_drop_offset', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:17 y:363
			OperatableStateMachine.add('DeactivateGripper',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'DeliverShipment', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})

			# x:16 y:286
			OperatableStateMachine.add('DeliverShipment',
										self.use_behavior(notify_shipment_readySM, 'DeliverShipment'),
										transitions={'finished': 'EndAssignment', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1003 y:297
			OperatableStateMachine.add('DetectCameraPart',
										DetectPartCameraAriacState(time_out=5.0),
										transitions={'continue': 'MoveR1PreGrasp1', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:18 y:215
			OperatableStateMachine.add('EndAssignment',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:17 y:579
			OperatableStateMachine.add('GetAgvPose',
										GetObjectPoseState(),
										transitions={'continue': 'ComuteDorp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'camera_ref_frame', 'frame': 'tray', 'pose': 'agv_pose'})

			# x:683 y:145
			OperatableStateMachine.add('GetBinFromLocations',
										GetItemFromListState(),
										transitions={'done': 'LookupCameraTopic', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'locations', 'index': 'zero', 'item': 'bin'})

			# x:675 y:585
			OperatableStateMachine.add('GetGripperState',
										GetVacuumGripperStatusState(),
										transitions={'continue': 'WachtEven', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'topic_name': 'gripper_status_topic', 'enabled': 'gripper_status_enabled', 'attached': 'gripper_status_attached'})

			# x:514 y:145
			OperatableStateMachine.add('GetPartLocation',
										GetMaterialLocationsState(),
										transitions={'continue': 'GetBinFromLocations'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part', 'material_locations': 'locations'})

			# x:1029 y:145
			OperatableStateMachine.add('LookupCameraFrame',
										LookupFromTableState(parameter_name='/ariac_tables', table_name='bin_configuration', index_title='bin', column_title='camera_frame'),
										transitions={'found': 'LookupPreGrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:864 y:148
			OperatableStateMachine.add('LookupCameraTopic',
										LookupFromTableState(parameter_name='/ariac_tables', table_name='bin_configuration', index_title='bin', column_title='camera_topic'),
										transitions={'found': 'LookupCameraFrame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:1028 y:222
			OperatableStateMachine.add('LookupPreGrasp',
										LookupFromTableState(parameter_name='/ariac_tables', table_name='bin_configuration', index_title='bin', column_title='robot_config'),
										transitions={'found': 'DetectCameraPart', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:353 y:143
			OperatableStateMachine.add('MoveR1Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPartLocation', 'planning_failed': 'WaitRetry1', 'control_failed': 'WaitRetry1', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_home', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:172 y:580
			OperatableStateMachine.add('MoveR1PreDrop',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetAgvPose', 'planning_failed': 'WaitRetry5', 'control_failed': 'WaitRetry5', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_tray1PreDrop', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1028 y:372
			OperatableStateMachine.add('MoveR1PreGrasp1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputePick', 'planning_failed': 'WaitRetry2', 'control_failed': 'WaitRetry2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:340 y:582
			OperatableStateMachine.add('MoveR1PreGrasp2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveR1PreDrop', 'planning_failed': 'WaitRetry4', 'control_failed': 'WaitRetry4', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:18 y:436
			OperatableStateMachine.add('MoveR1ToDrop',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'DeactivateGripper', 'planning_failed': 'WaitRetry6', 'control_failed': 'WaitRetry6'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1003 y:508
			OperatableStateMachine.add('MoveR1ToPick1',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'ActivateGripper', 'planning_failed': 'WaitRetry3', 'control_failed': 'ActivateGripper'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:165 y:144
			OperatableStateMachine.add('SetConveyorbeltPower',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'MoveR1Home', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'conveyor_belt_power'})

			# x:531 y:585
			OperatableStateMachine.add('WachtEven',
										WaitState(wait_time=1),
										transitions={'done': 'MoveR1PreGrasp2'},
										autonomy={'done': Autonomy.Off})

			# x:373 y:13
			OperatableStateMachine.add('WaitRetry1',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1Home'},
										autonomy={'done': Autonomy.Off})

			# x:1200 y:373
			OperatableStateMachine.add('WaitRetry2',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1PreGrasp1'},
										autonomy={'done': Autonomy.Off})

			# x:1198 y:507
			OperatableStateMachine.add('WaitRetry3',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1ToPick1'},
										autonomy={'done': Autonomy.Off})

			# x:356 y:652
			OperatableStateMachine.add('WaitRetry4',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1PreGrasp2'},
										autonomy={'done': Autonomy.Off})

			# x:176 y:653
			OperatableStateMachine.add('WaitRetry5',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1PreDrop'},
										autonomy={'done': Autonomy.Off})

			# x:203 y:405
			OperatableStateMachine.add('WaitRetry6',
										WaitState(wait_time=5),
										transitions={'done': 'MoveR1ToDrop'},
										autonomy={'done': Autonomy.Off})

			# x:869 y:584
			OperatableStateMachine.add('ActivateGripper',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'GetGripperState', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
