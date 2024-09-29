#MyState/RotEncoders.py
#-------------------------------------------------------------------------------


#=EasyEncoderIF
#===============================================================================
class EasyEncoderIF:
	"""NOTE
	- `id`: In `hanle_*` events meant for convenience when 1 class definition
	        is used with multiple buttons.
	"""
	#@abstractmethod
	def process_events(self, state_pressed):
		"""Also updates state-tracking data (Typically: Only run once per loop)"""
		pass

#User-facing event handlers (optionally/application-dependent)
#-------------------------------------------------------------------------------
	def handle_change(self, id, delta):
		"""Encoder accumulated a delta since last event"""
		pass


#=EasyEncoderIF
#===============================================================================
class EasyEncoder(EasyEncoderIF):
	"""EasyEncoder: Generic FSM implementation for interacting with rotary encoders
	(Must implement event handlers declared in interface `EasyButtonIF`.)
	"""
	#Finite State Machine (FSM) controlling interations with buttons
	def __init__(self, id=None):
		self.id = id

#Process change events
#-------------------------------------------------------------------------------
	def process_events(self, state_delta):
		if state_delta != 0:
			self.handle_change(self.id, state_delta)
