#CtrlInputWrap/NeoKey.py
#-------------------------------------------------------------------------------
from adafruit_neokey.neokey1x4 import NeoKey1x4
from MyState.CtrlInputs.Buttons import Profiles, EasyButton


#=EasyNeoKey
#===============================================================================
class EasyNeoKey_1x4:
	"""Convenience wrapper. Feel free to access `.btn` directly."""

	def __init__(self, oref:NeoKey1x4, btnCls, profile=Profiles.DEFAULT):
		"""btnCls: Derived class with custom event handlers."""
		super().__init__(profile)
		self.btns = tuple(btnCls(id=i, profile=profile) for i in range(4))
		self.oref = oref

	def _physcan_ispressed(self, idx):
		return self.oref[idx]

#Process inputs (and trigger events)
#-------------------------------------------------------------------------------
	def process_inputs_all(self):
		"""Also updates state (Typically: Only run once per loop)"""
		for b in self.btns:
			b:EasyButton
			isactive = self._physcan_ispressed(b.id)
			b.process_withinputs(isactive)
		return

#Last line
