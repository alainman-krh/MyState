#MyState/Predefined/RotEncoders.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.RotEncoders import EasyEncoder, EncoderSensorIF
from MyState.SigTools import SignalListenerIF
from MyState.Signals import SigValue


#=Convenient implementations of ::EasyEncoder
#===============================================================================
class EasyEncoder_Signal(EasyEncoder):
	"""Emits signals on position change"""
	def __init__(self, l:SignalListenerIF, section, id, encsense:EncoderSensorIF):
		super().__init__(id, encsense)
		self.l =l
		#Buffer signal to avoid re-creating:
		self.sig_change = SigValue(section, id+".change", val=0)

	def handle_change(self, id, delta):
		self.sig_change.val = delta
		self.l.process_signal(self.sig_change)
