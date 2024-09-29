#MyState/Predefined/Buttons.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Buttons import Profiles, EasyButton, ButtonSensorIF
from MyState.SigTools import SignalListenerIF
from MyState.Signals import SigAbstract, SigDirect


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
	
class EasyButton_SignalPressRel(EasyButton):
	"""Emits signals on press/release only (don't want to make too many objects)"""
	def __init__(self, id, btnsense:ButtonSensorIF, l:SignalListenerIF, section, profile=Profiles.DEFAULT):
		super().__init__(id, btnsense, profile=profile)
		self.l =l
		self.sig_press = SigDirect(section, "press_"+id)
		self.sig_release = SigDirect(section, "release_"+id)

	def handle_press(self, id):
		self.l.signal_process(self.sig_press)
	def handle_release(self, id):
		self.l.signal_process(self.sig_release)