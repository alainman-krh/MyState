#MyState/Predefined/RotEncoders.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.RotEncoders import EasyEncoder, EncoderSensorIF
from MyState.SigTools import SignalListenerIF
from MyState.Signals import SigIncrement


#=Convenient implementations of ::EasyEncoder
#===============================================================================
class EasyEncoder_Signal(EasyEncoder):
	"""Emits signals on position change"""
	def __init__(self, id, encsense:EncoderSensorIF, l:SignalListenerIF, section):
		super().__init__(id, encsense)
		self.l =l
		#Buffer signal to avoid re-creating:
		self.sig_change = SigIncrement(section, "change_"+id, val=0)

	def handle_change(self, id, delta):
		self.sig_change.val = delta
		self.l.signal_process(self.sig_change)
