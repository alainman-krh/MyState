#demos\NeoPixelControl_HomeAnalog\HAL_Macropad.py: Hardware Abstraction Layer
#-------------------------------------------------------------------------------
from MyState.Predefined.Buttons import EasyButton_SignalPressRel as KPButton
from MyState.CtrlInputs.Buttons import Profiles
from MyState.SigTools import SignalListenerIF
from CtrlInputWrap.Buttons import ButtonSensorDIO
from rotaryio import IncrementalEncoder
from neopixel import NeoPixel
import board, digitalio
r"""HAL layer helping to reduce complexity of interfacing with Adafruit Macropad"""


#==Constants
#===============================================================================
KEYPAD_SENSEPIN_LIST = ( #Pin references only. Does not directly measure input state:
	board.KEY1, board.KEY2, board.KEY3, board.KEY4, board.KEY5, board.KEY6,
	board.KEY7, board.KEY8, board.KEY9, board.KEY10, board.KEY11, board.KEY12,
)
KEYPAD_KEYCOUNT = len(KEYPAD_SENSEPIN_LIST)
KEYPAD_NPX = NeoPixel(board.NEOPIXEL, KEYPAD_KEYCOUNT) #One per key
KEYPAD_ENCODER = IncrementalEncoder(board.ENCODER_A, board.ENCODER_B)


#==KeypadElement
#===============================================================================
class KeypadElement:
	"""Pre-configured for macropad"""
	def __init__(self, idx, id, l:SignalListenerIF, section, profile=Profiles.DEFAULT):
		self.idx = idx
		pin = KEYPAD_SENSEPIN_LIST[idx]
		#Build/configure keysense pins:
		keysense = ButtonSensorDIO(pin, pull=digitalio.Pull.UP, active_low=True)
		self.btn = KPButton(id, keysense, l, section, profile)
	def pixel_set(self, value):
		"""Must be a tuple(R,G,B)"""
		KEYPAD_NPX[self.idx] = value


#==IncrEncoderSensor
#===============================================================================
from MyState.CtrlInputs.RotEncoders import EncoderSensorIF
class IncrEncoderSensor(EncoderSensorIF):
	"""Wraps `rotaryio.IncrementalEncoder`"""
	def __init__(self, sense:IncrementalEncoder, scale=1):
		self.sense = sense
		self.scale = -scale #IncrementalEncoder positions decrease in clockwise direction.
		self.poslast = 0
		self.read_delta() #Read to zero out initial postition

	def read_delta(self):
		"""From last time checked"""
		pos = self.sense.position #Assuming encoder rolls over??
		delta = pos - self.poslast #Magnitude can be >1 if multiple clicks processed between calls.
		self.poslast = pos
		return delta*self.scale
