#demos\AFMacropad_LightCtrl\HAL_Macropad.py: Hardware Abstraction Layer
#-------------------------------------------------------------------------------
from MyState.Predefined.Buttons import EasyButton_SignalPressRel
from MyState.CtrlInputs.Buttons import Profiles
from MyState.SigTools import SignalListenerIF
from CtrlInputWrap.digitalio import ButtonSensorDIO
from CtrlInputWrap.rotaryio import EncoderSensorRIO
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
KEYPAD_ENCODER = EncoderSensorRIO(board.ENCODER_A, board.ENCODER_B, scale=5)


#==KeypadElement
#===============================================================================
class KeypadElement:
	"""Pre-configured for macropad"""
	def __init__(self, l:SignalListenerIF, section, id, idx, profile=Profiles.DEFAULT):
		self.idx = idx
		pin = KEYPAD_SENSEPIN_LIST[idx]
		#Build/configure keysense pins:
		keysense = ButtonSensorDIO(pin, pull=digitalio.Pull.UP, active_low=True)
		self.btn = EasyButton_SignalPressRel(l, section, id, keysense, profile)
	def pixel_set(self, value):
		"""Must be a tuple(R,G,B)"""
		KEYPAD_NPX[self.idx] = value
