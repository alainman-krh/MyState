#MyState/RotEncoders.py
#-------------------------------------------------------------------------------


#=EasyEncoder
#===============================================================================
class EasyEncoder:
	"""EasyEncoder: Generic FSM implementation for interacting with rotary encoders.
	USAGE: User derives this `EasyEncoder` & implements custom `handle_*` functions.

	NOTE:
	- `id`: In `hanle_*` events meant for convenience when 1 class definition
	        is used with multiple buttons.
	"""
	#Finite State Machine (FSM) controlling interations with buttons
	def __init__(self, id=None):
		self.id = id

#User-facing event handlers (optional/application-dependent)
#-------------------------------------------------------------------------------
	def handle_change(self, id, delta):
		"""Encoder accumulated a delta since last event"""
		pass

#Process inputs (and trigger events)
#-------------------------------------------------------------------------------
	def process_withinputs(self, state_delta):
		"""Provide inputs explicitly"""
		sig_change = (state_delta != 0) #FSM signal
		if sig_change:
			self.handle_change(self.id, state_delta)

	def process_inputs(self):
		raise Exception("TODO")
