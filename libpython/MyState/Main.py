#MyState/State.py
#-------------------------------------------------------------------------------
from .Signals import SigAbstract, IOChanIF
from .Signals import SigUpdate, SigSet, SigGet, SigIncrement, SigToggle
from .Primitives import StateField_Int, FieldGroup
from .SigTools import SignalListenerIF
from . import SigTools

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
	def update(self, sig:SigUpdate):
		wasproc = False
		for l in self.observers:
			l:SignalListenerIF
			wasproc = l.update(sig)
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
			#TODO: reply to sig.iochan if exists
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

	def listeners_setlist(self, listener_list):
		self.listeners = listener_list
		self.stateblk_list = []
		for l in self.listeners:
			if type(l) is StateBlock:
				self.stateblk_list.append(l)
		self._cache_update()

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
				blk.process_signal(sig_update)
		return

#-------------------------------------------------------------------------------
	def _signal_process(self, sig:SigAbstract):
		wasproc = False
		sec = self.section_d.get(sig.section, None)
		if sec is None:
			return wasproc

		sec:StateBlock
		wasproc = sec.process_signal(sig)
		if wasproc:
			sec.state_invalidate()
		return wasproc

	def process_signal(self, sig:SigAbstract, update_now=True):
		wasproc = False
		if update_now:
			self.stateblocks_setvalid()
			wasproc = self._signal_process(sig)
			self.stateblocks_updateinvalid()
		else:
			wasproc = self._signal_process(sig)
		return wasproc

#-------------------------------------------------------------------------------
	def _signal_process_str(self, sig_str:str, iochan:IOChanIF=None):
		success = True
		siglist = SigTools.Signal_Deserialize(sig_str, iochan=iochan)
		for sig in siglist:
			wasproc = self.process_signal(sig)
			success &= wasproc
		return success

	def signal_process_str(self, sig_str:str, update_now=True, iochan:IOChanIF=None):
		success = False
		if update_now:
			self.stateblocks_setvalid()
			success = self._signal_process_str(sig_str, iochan=iochan)
			self.stateblocks_updateinvalid()
		else:
			success = self._signal_process_str(sig_str, iochan=iochan)
		return success

#-------------------------------------------------------------------------------
	def signal_process_script(self, script:str):
		success = True
		self.stateblocks_setvalid()
		for line in script.splitlines():
			success &= self._signal_process_str(line)
		self.stateblocks_updateinvalid()
		return success
