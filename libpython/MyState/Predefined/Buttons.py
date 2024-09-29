#MyState/Predefined/Buttons.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Buttons import Profiles, EasyButton
from MyState.SigTools import SignalListenerIF
from MyState.Signals import SigAbstract


#=Convenient ::EasyButton
#===============================================================================
class EasyButton_Press(EasyButton):
	"""Reacts to button press (down) only"""
	def __init__(self, l:SignalListenerIF, sig:SigAbstract, profile=Profiles.DEFAULT):
		super().__init__(id=None, profile=profile)
		self.l =l
		self.sig = sig

	def handle_press(self, id):
		self.l.signal_process(self.sig)

class EasyButton_Release(EasyButton):
	"""Reacts to button released only"""
	def __init__(self, l:SignalListenerIF, sig:SigAbstract, profile=Profiles.DEFAULT):
		super().__init__(id=None, profile=profile)
		self.l =l
		self.sig = sig

	def handle_release(self, id):
		self.l.signal_process(self.sig)