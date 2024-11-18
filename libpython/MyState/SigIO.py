#MyState/SigIO.py
#-------------------------------------------------------------------------------
from .Signals import SigUpdate, SigSet, SigGet, SigIncrement, SigToggle
from .Signals import SigAbstract, SigValue, SigDump, MSG_SIGACK
from .SigTools import SignalListenerIF, Signal_Deserialize


#==Constants
#===============================================================================
MSGDUMP_EOT = "DMP EOT"


#==SigIOIF
#===============================================================================
class SigIOIF:
	r"""Standard way to interface with IO com channels used for signalling
	(Split out from SigIOController for readability purposes)

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


#==SigIOController
#===============================================================================
class SigIOController(SigIOIF):
	r"""
	TODO:
	- Find a way NOT to create list of signals when reading IO-stream (using Signal_Deserialize).
	- Likely beneficial to minimize allocations."""

	def __init__(self, listener:SignalListenerIF=None):
		self.listener = listener
		self.cache_siglist = None #Unprocessed signals/messages
		self.cache_sigval = SigValue("","",0) #For sending OUT signals

#-------------------------------------------------------------------------------
	def _cache_siglist_pop(self):
		siglist = self.cache_siglist
		if siglist is None or len(siglist) < 1:
			return None

		sig = siglist[0]
		self.cache_siglist = None if (len(siglist) < 2) else siglist[1:] #Update cache
		return sig

#-------------------------------------------------------------------------------
	def send_signal(self, sig:SigAbstract, block=True):
		"""Send a signal through this IO interface.
		- block: =False: non-blocking

		Returns SigValue (return for SigGet), True for simple Signal ack, or None on error/timeout
		"""
		msgstr = sig.serialize()
		if not block:
			self.write("!")
			self.write(msgstr)
			return True #Assume worked
		needsval = (type(sig) is SigGet)

		self.write(msgstr)
		ans_str = self.readline_block() #Might timeout, get bad response, etc (must keep going)
		if ans_str is None:
			return None #Error
		ans_str = ans_str.strip()
		ans_sig = Signal_Deserialize(ans_str)
		if needsval:
			if type(ans_sig) != SigValue:
				return None #Error
			else:
				return ans_sig.val
		#Simple ack expected (else: None):
		result = (MSG_SIGACK == ans_str)
		return result

#-------------------------------------------------------------------------------
	def _signal_dump(self, sig:SigDump):
		#.listener actually needs to be a `ListenerRoot` - or a StateControllerIF maybe (TODO)???
		msg_list = self.listener.state_getdump(sig.section)
		for msg in msg_list:
			self.write(msg); self.write("\n")
		self.write(MSGDUMP_EOT); self.write("\n")
		return True #wasproc

	def _signal_get(self, sig:SigAbstract):
		val = 0 #TODO: Call self.listener.GET here!!!
		if val is None:
			self.write(MSG_SIGACK); self.write("\n") #Need some reply
			return False #wasproc
		self.cache_sigval.id = sig.id
		self.cache_sigval.section = sig.section
		self.cache_sigval.val = val
		msgval = self.cache_sigval.serialize()
		self.write(msgval); self.write("\n")
		return True #wasproc

	def _process_signal_list(self, siglist):
		success = True
		for sig in siglist: #A single signal can have multiple components (ex: R,G,B)
			if type(sig) is SigGet:
				wasproc = self._signal_get(sig)
			elif type(sig) is SigDump:
				wasproc = self._signal_dump(sig)
			else:
				wasproc = self.listener.process_signal(sig)
				#Acknowledge signal even if not detected:
				self.write(MSG_SIGACK); self.write("\n")
			success &= wasproc
		return success

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
		msgstr = self.readline_noblock()
		if msgstr is None:
			return None
		msgstr = msgstr.strip()
		self.cache_siglist = Signal_Deserialize(msgstr)
		sig = self._cache_siglist_pop()
		return sig

#-------------------------------------------------------------------------------
	def process_signals(self):
		"""Process any incomming signals

		Requires: `.listener` defined (!= None)
		"""
		success = True

		#Process remaining messages in cache first
		siglist = self.cache_siglist
		if siglist != None:
			success &= self._process_signal_list(siglist)
		self.cache_siglist = None #Update: No un-processed signals

		#Process any new messages:
		while True:
			msgstr = self.readline_noblock()
			if msgstr is None:
				break #Done
			msgstr = msgstr.strip()
			siglist = Signal_Deserialize(msgstr)
			success &= self._process_signal_list(siglist)
		return success


#==SigIOScript
#===============================================================================
class SigIOScript(SigIOController):
	"""Read a script from a string"""
	def __init__(self, listener:SignalListenerIF, scriptlines=tuple()):
		super().__init__(listener)
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

#Last line