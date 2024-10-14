#MyState/State.py
#-------------------------------------------------------------------------------
from .Signals import SigUpdate, SigSet, SigGet, SigIncrement, SigToggle
from .Signals import SigAbstract, SigValue, SigDump
from .Primitives import StateField_Int, FieldGroup
from .SigTools import SignalListenerIF
from .SigIO import SigIOScript
import io

r"""Info relating to state
Consider: 'SET Main:kitchen.enabled 1'
- Section = "Main", id = "kitchen.enabled", value = 1
"""


#==StateBlock
#===============================================================================
class StateBlock(SignalListenerIF):
	def __init__(self, id, field_list):
		self.id = id
		self.field_list_set(field_list)
		self.observers = []
		self.state_valid = True

#-------------------------------------------------------------------------------
	def _cache_update(self):
		"""Updates cache of sub-structures"""
		self.field_d = {}
		for f in self.field_list:
			if type(f) is FieldGroup:
				grp:FieldGroup = f
				for fi in grp.field_list:
					id = f"{grp.id}.{fi.id}"
					self.field_d[id] = fi
			else:
				self.field_d[f.id] = f

	def field_list_set(self, field_list):
		self.field_list = field_list
		self._cache_update()

	def field_list_strbygrp(self):
		result = []
		for f in self.field_list:
			if type(f) is FieldGroup:
				grp:FieldGroup = f
				subfid_list = tuple(subf.id for subf in grp.field_list)
				subf_str = ",".join(subfid_list)
				id = f"{grp.id}.({subf_str})"
				result.append(id)
			else:
				f:StateField_Int
				result.append(f.id)
		return result

#-------------------------------------------------------------------------------
	def state_invalidate(self):
		self.state_valid = False

	def observers_add(self, l:SignalListenerIF):
		self.observers.append(l)

#-------------------------------------------------------------------------------
	def state_getdump(self):
		"""Returns a list of `SigValue` message strings representing state."""
		result = []
		sigbuf = SigValue(self.id, "", 0)
		for f in self.field_list:
			if type(f) is FieldGroup:
				grp:FieldGroup = f
				subfid_list = tuple(subf.id for subf in grp.field_list)
				subf_str = ",".join(subfid_list)
				sigbuf.id = f"{grp.id}.({subf_str})"
				val_list = tuple(str(subf.val) for subf in grp.field_list)
				val_str = ",".join(val_list)
				sigbuf.val = f"({val_str})"
				result.append(sigbuf.serialize())
			else:
				f:StateField_Int
				sigbuf.id = f.id; sigbuf.val = f.val
				result.append(sigbuf.serialize())
		return result

#-------------------------------------------------------------------------------
	def update(self, sig:SigUpdate):
		wasproc = False
		for l in self.observers:
			l:SignalListenerIF
			result = (l.update(sig) == True) #Safety: Might not return bool
			wasproc |= result #If anything updates - that's good
		return wasproc

#-------------------------------------------------------------------------------
	def process_signal(self, sig:SigAbstract):
		wasproc = False
		T = type(sig)
		if T is SigUpdate:
			return self.update(sig)
		field:StateField_Int = self.field_d.get(sig.id, None)
		if field is None:
			return wasproc

		if T is SigSet:
			field.valset(sig.val)
			self.state_invalidate()
		elif T is SigIncrement:
			field.valinc(sig.val)
			self.state_invalidate()
		elif T is SigToggle:
			field.valtoggle()
			self.state_invalidate()
		elif T is SigGet:
			v = field.valget()
			print(f"DBG/ {sig.id}: {v}")
			#TODO: IGNORE - need special get function!
		else:
			return wasproc
		wasproc = True
		return wasproc


#==ListenerRoot
#===============================================================================
class ListenerRoot(SignalListenerIF):
	def __init__(self, listener_list):
		self.listeners_setlist(listener_list)

#-------------------------------------------------------------------------------
	def _cache_update(self):
		"""Updates cache of sub-structures"""
		self.section_d = {l.id: l for l in self.listeners}
		self.sig_update = SigUpdate("", "")

	def listeners_setlist(self, listener_list):
		self.listeners = listener_list
		self.stateblk_list = []
		for l in self.listeners:
			if type(l) is StateBlock:
				self.stateblk_list.append(l)
		self._cache_update()

#-------------------------------------------------------------------------------
	def update(self, sig:SigUpdate):
		"""Update all state blocks"""
		wasproc = False
		for blk in self.stateblk_list:
			blk:StateBlock
			self.sig_update.id = blk.id
			wasproc &= blk.update(self.sig_update) #All should update
		return wasproc

#-------------------------------------------------------------------------------
	def stateblocks_setvalid(self):
		for blk in self.stateblk_list:
			blk:StateBlock
			blk.state_valid = True

	def stateblocks_updateinvalid(self):
		for blk in self.stateblk_list:
			blk:StateBlock
			if not blk.state_valid:
				sig_update = SigUpdate(blk.id, "")
				blk.update(sig_update)
		return

#-------------------------------------------------------------------------------
	def state_getdump(self, section):
		stateblk_list = []
		stateblk = self.section_d.get(section, None)
		if ("ROOT" == section): #Meant for "ListenerRoot" (this)
			stateblk_list = self.stateblk_list #All state blocks
		elif stateblk != None:
			stateblk_list = [stateblk]

		result = []
		for blk in stateblk_list:
			blk:StateBlock
			result.extend(blk.state_getdump())
		return result

#-------------------------------------------------------------------------------
	def _process_signal_core(self, sig:SigAbstract):
		wasproc = False
		section = self.section_d.get(sig.section, None)
		if section is None:
			return wasproc

		section:StateBlock
		wasproc = section.process_signal(sig)
		if wasproc:
			section.state_invalidate()
		return wasproc

	def process_signal(self, sig:SigAbstract, update_now=True):
		wasproc = False
		if update_now:
			self.stateblocks_setvalid()
			wasproc = self._process_signal_core(sig)
			self.stateblocks_updateinvalid()
		else:
			wasproc = self._process_signal_core(sig)
		return wasproc

#-------------------------------------------------------------------------------
	def script_load(self, filepath:str):
		scriptlines = None
		self.stateblocks_setvalid()

		with io.open(filepath, "r") as fio:
			scriptlines = fio.readlines()
		script = SigIOScript(self, scriptlines)
		success = script.process_signals()

		self.stateblocks_updateinvalid()
		return success