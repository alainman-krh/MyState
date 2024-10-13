#demos\LightCtrlMP_AFMacropad\HAL_Macropad.py: Hardware Abstraction Layer
#-------------------------------------------------------------------------------
from CtrlInputWrap.rotaryio import EncoderSensorRIO
from neopixel import NeoPixel
import keypad #Detects press/release events!
import board
r"""HAL layer helping to reduce complexity of interfacing with Adafruit Macropad"""


#==Constants
#===============================================================================
KEYPAD_SENSEPIN_LIST = ( #Pin references only. Does not directly measure input state:
	board.KEY1, board.KEY2, board.KEY3, board.KEY4, board.KEY5, board.KEY6,
	board.KEY7, board.KEY8, board.KEY9, board.KEY10, board.KEY11, board.KEY12,
)
KEYPAD_KEYCOUNT = len(KEYPAD_SENSEPIN_LIST)
KEYPAD_NPX = NeoPixel(board.NEOPIXEL, KEYPAD_KEYCOUNT) #One per key
KEYPAD_ENCODER = EncoderSensorRIO(board.ENCODER_A, board.ENCODER_B, scale=5)


#==KeypadElement
#===============================================================================
class KeypadElement:
	"""Pre-configured for macropad. Also controls associated neopixel"""
	def __init__(self, idx):
		self.idx = idx
		pin = KEYPAD_SENSEPIN_LIST[idx]
		#Build/configure keysense pins:
		self.key = keypad.Keys([pin], value_when_pressed=False, pull=True)
		self.events = self.key.events #Alias makes user code more readable
	def pixel_set(self, value):
		"""Must be a tuple(R,G,B)"""
		KEYPAD_NPX[self.idx] = value
