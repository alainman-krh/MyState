#CtrlInputWrap/rotaryio.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.RotEncoders import EncoderSensorIF
from rotaryio import IncrementalEncoder

r"""HACK INFO (Circuit Python 9.1.4)
- IncrementalEncoder keeps incrementing all the way to +/-maxint ((1<<31)-1).
- Will roll over to negative values (and vice-versa) - will NOT saturate.
- HACK: reset .position = 0 after reading. WARN: Might swallow some readings.
- Hack necessary because Python largeint behaves strangely @ roll-over.
"""

#==EncoderSensorRIO
#===============================================================================
class EncoderSensorRIO(EncoderSensorIF):
	"""Wraps `rotaryio.IncrementalEncoder`."""
	def __init__(self, pin_a, pin_b, scale=1):
		self.sense = IncrementalEncoder(pin_a, pin_b)
		self.scale = -scale #IncrementalEncoder positions decrease in clockwise direction.
		self.read_delta() #Read to zero out initial postition

	def read_delta(self):
		"""From last time checked (resets .position)"""
		#Magnitude can be >1 if multiple clicks processed between calls:
		delta = self.sense.position
		if delta != 0:
			self.sense.position = 0 #Hack: rolls over @ (1<<31)-1 (never saturates).
			#Don't reset position unless delta found (less likely to miss a click)
		return delta*self.scale
