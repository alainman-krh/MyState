#demos\NeoPixelControl_HomeAnalog\HAL_Macropad.py: Hardware Abstraction Layer
#-------------------------------------------------------------------------------
from MyState.Predefined.Buttons import EasyButton_SignalPressRel as KPButton
from MyState.CtrlInputs.Buttons import Profiles, ButtonSensorIF
from MyState.Predefined.RotEncoders import EasyEncoder_Incr
from MyState.SigTools import SignalListenerIF
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


#==ButtonSensorDIO
#===============================================================================
from MyState.CtrlInputs.Buttons import ButtonSensorIF
class ButtonSensorDIO(ButtonSensorIF):
	def __init__(self, pin, pull=digitalio.Pull.UP, active_low=False):
		#Configure pin for sensing:
		self.btnsense = digitalio.DigitalInOut(pin)
		self.btnsense.direction = digitalio.Direction.INPUT
		self.btnsense.pull = pull
		self.activeval = False if active_low else True
	def isactive(self):
		"""Is button active (typ: pressed)?"""
		return self.btnsense.value == self.activeval


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


#==RotaryEncoder_Delta
#===============================================================================
class EncoderSense:
	"""Generic rotaryio wrapper to get back difference in position between current and last"""
	def __init__(self, sense:IncrementalEncoder, handler:EasyEncoder_Incr, scale=1):
		self.sense = sense
		self.handler = handler #Ref mostly for convenience
		self.scale = -scale #IncrementalEncoder positions decrease in clockwise direction.
		self.poslast = 0
		self.pos_getdelta() #Zero out postition

	def pos_getdelta(self):
		"""From last time checked?"""
		pos = self.sense.position #Assuming encoder rolls over??
		delta = pos - self.poslast #Can be larger than 1
		self.poslast = pos
		return delta*self.scale
