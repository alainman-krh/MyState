#CtrlInputWrap/rotaryio.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.RotEncoders import EncoderSensorIF
from rotaryio import IncrementalEncoder


#==EncoderSensorRIO
#===============================================================================
class EncoderSensorRIO(EncoderSensorIF):
	"""Wraps `rotaryio.IncrementalEncoder`."""
	def __init__(self, pin_a, pin_b, scale=1):
		self.sense = IncrementalEncoder(pin_a, pin_b)
		self.scale = -scale #IncrementalEncoder positions decrease in clockwise direction.
		self.poslast = 0
		self.read_delta() #Read to zero out initial postition

	def read_delta(self):
		"""From last time checked"""
		pos = self.sense.position #Assuming encoder rolls over??
		delta = pos - self.poslast #Magnitude can be >1 if multiple clicks processed between calls.
		self.poslast = pos
		return delta*self.scale
