#MyState/RotEncoders.py
#-------------------------------------------------------------------------------

#=EncoderSensorIF
#===============================================================================
class EncoderSensorIF:
	#@abstractmethod
	def read_delta(self):
		#Some interrupt-assisted encoders might read multiple steps between
		#2 calls to EasyEncoder.process_inputs()
		pass


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
	def __init__(self, id=None, encsense:EncoderSensorIF=None):
		self.id = id
		self.encsense = encsense

#User-facing event handlers (optional/application-dependent)
#-------------------------------------------------------------------------------
	def handle_change(self, id, delta):
		"""Encoder accumulated a delta since last event"""
		pass

#Process inputs (and trigger events)
#-------------------------------------------------------------------------------
	def process_giveninputs(self, delta_accrued): #delta_accrued: since last call
		"""Provide inputs explicitly"""
		sig_change = (delta_accrued != 0) #FSM signal
		if sig_change:
			self.handle_change(self.id, delta_accrued)

	def process_inputs(self):
		delta_accrued = self.encsense.read_delta() #`.encsense` must be specified to call.
		self.process_giveninputs(delta_accrued)
