#MyState/Primitives.py
#-------------------------------------------------------------------------------
from .SigTools import SignalListenerIF, cliprng

class StateField_Abstract(SignalListenerIF):
	#TODO: Needed???
	pass

class StateField_Int:
	def __init__(self, id, vmin, vmax, dflt=None):
		if dflt is None:
			dflt = vmin
		self.id = id
		self.range = (vmin, vmax)
		self.val = dflt

	def valset(self, val):
		self.val = cliprng(self.range, val)
		return self.val

	def valget(self):
		return self.val

	def valinc(self, val):
		return self.valset(self.val+val)

	def valtoggle(self):
		valnew = self.range[0] #Try min first
		if valnew == self.val: #Toggle to max instead
			valnew = self.range[1]
		return self.valset(valnew)

class FieldGroup:
	def __init__(self, id, field_list):
		self.id = id
		self.field_list = field_list
