#MyState/Predefined/Buttons.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Buttons import Profiles, EasyButton, ButtonSensorIF
from MyState.SigTools import SignalListenerIF
from MyState.Signals import SigEvent


#=Convenient implementations of ::EasyButton
#===============================================================================
class EasyButton_SignalPressRel(EasyButton):
	"""Emits signals on press/release only (don't want to make too many objects)"""
	def __init__(self, l:SignalListenerIF, section, id, btnsense:ButtonSensorIF, profile=Profiles.DEFAULT):
		super().__init__(id, btnsense, profile=profile)
		self.l =l
		self.sig_press = SigEvent(section, id+".press")
		self.sig_release = SigEvent(section, id+".release")
	def handle_press(self, id):
		self.l.process_signal(self.sig_press)
	def handle_release(self, id):
		self.l.process_signal(self.sig_release)