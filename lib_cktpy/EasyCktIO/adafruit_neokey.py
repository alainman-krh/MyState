#EasyCktIO/adafruit_neokey.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Buttons import EasyButton, ButtonSensorIF, Profiles
from adafruit_neokey.neokey1x4 import NeoKey1x4

#TODO: Cleanup. Hierarchy somewhat inverted (not practcial)


#=EasyNeoKey
#===============================================================================
class NeoKeySensorIF(ButtonSensorIF):
	def __init__(self, oref:NeoKey1x4, idx):
		self.oref = oref
		self.idx = idx

	def isactive(self):
		return self.oref[self.idx]


#=EasyNeoKey
#===============================================================================
class EasyNeoKey_1x4:
	"""Convenience wrapper. Feel free to access `.btn` directly."""

	def __init__(self, oref:NeoKey1x4, btnCls:EasyButton, profile=Profiles.DEFAULT):
		"""btnCls: Derived class with custom event handlers."""
		self.keys = tuple(btnCls(idx, NeoKeySensorIF(oref, idx), profile=profile) for idx in range(4))

#Process inputs (and trigger events)
#-------------------------------------------------------------------------------
	def process_inputs_all(self):
		"""Also updates state (Typically: Only run once per loop)"""
		for b in self.keys:
			b:EasyButton
			b.process_inputs()
		return

#Last line