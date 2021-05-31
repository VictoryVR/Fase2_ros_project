#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.message_state import MessageState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Apr 27 2021
@author: Gerard Harkema
'''
class lookup_table_exampleSM(Behavior):
	'''
	Example to lookup form table in parameter_server
	'''


	def __init__(self):
		super(lookup_table_exampleSM, self).__init__()
		self.name = 'lookup_table_example'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:763 y:63, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.index_value = 'bin4'
		_state_machine.userdata.column_value = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:227 y:40
			OperatableStateMachine.add('LookupFromTable',
										LookupFromTableState(parameter_name='/ariac_tables', table_name='bin_configuration', index_title='bin', column_title='camera_frame'),
										transitions={'found': 'ColumnValueMessage', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'index_value', 'column_value': 'column_value'})

			# x:479 y:42
			OperatableStateMachine.add('ColumnValueMessage',
										MessageState(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'column_value'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
