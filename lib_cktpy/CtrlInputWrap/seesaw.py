#CtrlInputWrap/seesaw.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.RotEncoders import EncoderSensorIF
from adafruit_seesaw.rotaryio import IncrementalEncoder as IEncoderSS
from adafruit_seesaw.seesaw import Seesaw


r"""HACK INFO (Circuit Python 9.1.4)
- IncrementalEncoder keeps incrementing all the way to +/-maxint ((1<<31)-1).
- Will roll over to negative values (and vice-versa) - will NOT saturate.
- HACK: reset .position = 0 after reading. WARN: Might swallow some readings.
- Hack preferable because Python largeint behaves strangely @ roll-over.
"""


#==Constants
#===============================================================================
DEFAULTI2CADDR_SEESAW = 0x49 #Default I2C address of Seesaw on "NeoRotary 4" (AF #5752)


#==EncoderSensorRIO
#===============================================================================
class EncoderSensorRIO(EncoderSensorIF):
	"""Wraps `adafruit_seesaw.rotaryio.IncrementalEncoder`."""
	def __init__(self, seesaw:Seesaw, idx=0, scale=1):
		self.sense = IEncoderSS(seesaw, idx) #Won't actually use this
		self.seesaw = seesaw
		self.idx = idx
		self.scale = scale #Seesaw/IncrementalEncoder positions INCREASES in clockwise direction.
		self.read_delta() #Read to zero out initial postition

	def read_delta(self):
		"""From last time checked (resets .position)"""
		#NOTE: NOT using `.sense:IEncoderSS`: No way to read delta. Reading directly from .seesaw.

		#Magnitude can be >1 if multiple clicks processed between calls:
		delta = self.seesaw.encoder_delta(self.idx) #Assuming handles rollover correctly (not verified)
		return delta*self.scale
