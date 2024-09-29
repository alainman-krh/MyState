#MyState/Predefined/RotEncoders.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.RotEncoders import EasyEncoder
from MyState.SigTools import SignalListenerIF
from MyState.Signals import SigIncrement


#=Convenient ::EasyEncoder
#===============================================================================
class EasyEncoder_Incr(EasyEncoder):
	"""Reacts to changes, and sends out SigIncrement"""
	def __init__(self, l:SignalListenerIF, sig:SigIncrement):
		super().__init__(id=None)
		self.l =l
		self.sig = sig

	def handle_change(self, id, delta):
		self.sig.val = delta #What to send
		self.l.signal_process(self.sig)
