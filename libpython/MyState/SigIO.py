#MyState/SigIO.py
#-------------------------------------------------------------------------------
from .Signals import SigUpdate, SigSet, SigGet, SigIncrement, SigToggle
from .Signals import SigAbstract, SigValue, SigDump
from .SigTools import SignalAwareStateIF, Signal_Deserialize


#==Constants
#===============================================================================
MSGDUMP_EOT = "DMP EOT"
MSG_SIGACK = "ACK" #For blocking transmissions (if not returning SigValue)


#==SigIOIF
#===============================================================================
class SigIOIF:
	r"""Standard way to interface with IO com channels used for signalling
	IMPORTANT: Implementation should provide a reasonable timeout value for .readline_block().
	"""
	#@abstractmethod #Doesn't exist
	def readline_noblock(self):
		#Returns `None` if data not yet available
		pass

	def readline_block(self):
		pass

	def write(self, msgstr):
		pass


#==SigCom
#===============================================================================
class SigCom:
	r"""Base "signal" communication layer.
	TODO:
	- Find a way NOT to create list of signals when reading IO-stream (using Signal_Deserialize).
	- Likely beneficial to minimize allocations."""

	def __init__(self, io:SigIOIF):
		self.io = io
		self.cache_siglist = None #Unprocessed signals/messages
		self.cache_sigval = SigValue("", "", 0) #For sending OUT signals

#-------------------------------------------------------------------------------
	def _cache_siglist_pop(self):
		siglist = self.cache_siglist
		if siglist is None or len(siglist) < 1:
			return None

		sig = siglist[0]
		self.cache_siglist = None if (len(siglist) < 2) else siglist[1:] #Update cache
		return sig

	def _cache_siglist_append(self, siglist):
		if self.cache_siglist is None:
			self.cache_siglist = siglist
			return
		if (siglist is None) or (len(siglist) < 1):
			return #Nothing to append
		self.cache_siglist.extend(siglist)

#-------------------------------------------------------------------------------
	def send_signal(self, sig:SigAbstract):
		"""Send a signal through this IO interface.
		Blocks on SigGet for a limited amount of time (don't hang).

		Returns SigValue (return for SigGet), True for simple Signal ack, or None on error/timeout.
		"""
		needsval = (type(sig) is SigGet)
		block = needsval #Might decouple in future - but now: only block (for limited time) on SigGet.

		msgstr = sig.serialize()
		if not block:
			#self.io.write("!") #TODO: Have a flag to indicate non-blocking?
			self.io.write(msgstr)
			return True #Assume worked

		#self.io.write("?") #TODO: Have a flag to indicate blocking/needing response?
		self.io.write(msgstr)
		ans_str = self.io.readline_block() #Might timeout, get bad response, etc (must keep going)
		if ans_str is None:
			return None #Error
		ans_str = ans_str.strip()
		siglist_new = Signal_Deserialize(ans_str) #Check for new signals
		ans_sig = siglist_new[-1] #Last element likely the answer.
		if needsval: #Currently suports: SigGet / expecting SigValue
			issought = False #Recieved what we asked?
			if (SigValue == type(ans_sig)) and (ans_sig.section == sig.id) and (ans_sig.id == sig.id):
				issought = True

			if issought:
				self._cache_siglist_append(siglist_new[:-1])
				return ans_sig.val
			else:
				#Don't try too hard. Can't guarantee signal order
				self._cache_siglist_append(siglist_new)
				return None #Error

		#Simple ack expected (else: None):
		result = (MSG_SIGACK == ans_str)
		return result

#-------------------------------------------------------------------------------
	def getvalue_orhang(self, sig:SigGet):
		"Will try until succeeds"
		#TODO? Is this a good idea?
		pass

#-------------------------------------------------------------------------------
	def read_signal_next(self):
		"""Read next signal (one at a time).
		Returns: None or one of `SigAbstract`.
		"""
		#Process remaining messages in cache first:
		sig = self._cache_siglist_pop()
		if sig != None:
			return sig

		#Look for new signals:
		msgstr = self.io.readline_noblock()
		if msgstr is None:
			return None
		msgstr = msgstr.strip()
		self.cache_siglist = Signal_Deserialize(msgstr)
		sig = self._cache_siglist_pop()
		return sig


#==SigLink
#===============================================================================
class SigLink(SigCom): #Must implement SigIOIF
	r"""Establishes a direct link between `SigIO` and `SignalAwareStateIF`."""

	def __init__(self, io:SigIOIF, state:SignalAwareStateIF):
		super().__init__(io)
		self.state = state

#-------------------------------------------------------------------------------
	def _signal_dump(self, sig:SigDump):
		msg_list = self.state.state_getdump(sig.section)
		for msg in msg_list:
			self.io.write(msg); self.io.write("\n")
		self.io.write(MSGDUMP_EOT); self.io.write("\n")
		return True #wasproc

#-------------------------------------------------------------------------------
	def _signal_get(self, sig:SigGet):
		val = self.state.state_getval(sig.section, sig.id)
		if val is None:
			self.io.write(MSG_SIGACK); self.io.write("\n") #Need some reply
			return False #wasproc
		self.cache_sigval.id = sig.id
		self.cache_sigval.section = sig.section
		self.cache_sigval.val = val
		msgval = self.cache_sigval.serialize()
		self.io.write(msgval); self.io.write("\n")
		return True #wasproc

#-------------------------------------------------------------------------------
	def _process_signal_list(self, siglist):
		success = True
		for sig in siglist: #A single signal can have multiple components (ex: R,G,B)
			if type(sig) is SigGet:
				wasproc = self._signal_get(sig)
			elif type(sig) is SigDump:
				wasproc = self._signal_dump(sig)
			else:
				wasproc = self.state.process_signal(sig)
				#Acknowledge signal even if not detected:
				self.io.write(MSG_SIGACK); self.io.write("\n")
			success &= wasproc
		return success

#-------------------------------------------------------------------------------
	def process_signals(self):
		"""Process any incomming signals"""
		success = True

		#Process remaining messages in cache first
		siglist = self.cache_siglist
		if siglist != None:
			success &= self._process_signal_list(siglist)
		self.cache_siglist = None #Update: No un-processed signals

		#Process any new messages:
		while True:
			msgstr = self.io.readline_noblock()
			if msgstr is None:
				break #Done
			msgstr = msgstr.strip()
			siglist = Signal_Deserialize(msgstr)
			success &= self._process_signal_list(siglist)
		return success


#==SigIO_Script/SigCom_Script/SigLink_Script
#===============================================================================
class SigIO_Script(SigIOIF):
	"""Implement SigIOIF from a "script" (list of "signal" strings)"""
	def __init__(self, scriptlines=tuple()):
		self.setscript_lines(scriptlines)

#-------------------------------------------------------------------------------
	def setscript_lines(self, scriptlines):
		"Set the script from a list of lines"
		if type(scriptlines) not in (list, tuple):
			raise Exception("Not a proper script")
		self.scriptlines = scriptlines
		self.idx = 0

	def setscript_str(self, script_str:str):
		"""Set the script from a string"""
		self.setscript_lines(script_str.splitlines())

#Implement SigIOIF interface:
#-------------------------------------------------------------------------------
	def readline_noblock(self):
		if self.idx >= len(self.scriptlines):
			return None
		line = self.scriptlines[self.idx]
		self.idx += 1
		return line

	def readline_block(self):
		return None #ACKs not supported in scripts

	def write(self, msgstr): #Not really supported
		return

#Convenience constructors
#-------------------------------------------------------------------------------
def SigCom_Script(scriptlines=tuple()):
	io = SigIO_Script(scriptlines)
	return SigCom(io)
def SigLink_Script(state:SignalAwareStateIF, scriptlines=tuple()):
	io = SigIO_Script(scriptlines)
	return SigLink(io, state)

#Last line