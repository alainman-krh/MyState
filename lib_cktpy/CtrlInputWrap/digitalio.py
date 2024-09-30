#CtrlInputWrap/digitalio.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Buttons import ButtonSensorIF
import digitalio


#==ButtonSensorDIO
#===============================================================================
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

#Last line