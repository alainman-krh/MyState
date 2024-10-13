#MyState/SigIO.py
#-------------------------------------------------------------------------------
from .Signals import SigUpdate, SigSet, SigGet, SigIncrement, SigToggle
from .Signals import SigAbstract, SigValue, MSG_SIGACK
from .SigTools import SignalListenerIF, Signal_Deserialize


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
		#Returns SigValue (return for SigGet), True for simple Signal ack, or None on error/timeout
		pass

	def write(self, msgstr):
		pass


#==SigIOController
#===============================================================================
class SigIOController(SigIOIF):
	def __init__(self, listener:SignalListenerIF):
		self.listener = listener
		self.cache_sigval = SigValue("","",0)

#-------------------------------------------------------------------------------
	def send_signal(self, sig:SigAbstract, block=True):
		"""Send a signal through this IO interface.
		- block: =False: non-blocking
		"""
		msgstr = sig.serialize()
		if not block:
			self.write("!")
			self.write(msgstr)
			return True #Assume worked
		needsval = (type(sig) is SigGet)

		self.write(msgstr)
		result = self.readline_block() #Might timeout, get bad response, etc
		if needsval:
			if type(result) != SigValue:
				return None #Error
			else:
				return result.val
		#Simple ack expected (else: None):
		if result != True:
			result = None
		return result

#-------------------------------------------------------------------------------
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

	def _process_signal_str(self, msgstr:str):
		success = True
		siglist = Signal_Deserialize(msgstr)
		for sig in siglist: #A single signal can have multiple components (ex: R,G,B)
			if type(sig) is SigGet:
				wasproc = self._signal_get(sig)
			else:
				wasproc = self.listener.process_signal(sig)
				#Acknowledge signal even if not detected:
				self.write(MSG_SIGACK); self.write("\n")
			success &= wasproc
		return success

#-------------------------------------------------------------------------------
	def process_signals(self):
		"""Process any incomming signals"""
		success = True
		while True:
			msgstr = self.readline_noblock()
			if msgstr is None:
				break #Done
			success &= self._process_signal_str(msgstr)
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
		return self.readline_noblock()

	def write(self, msgstr): #Not really supported
		return

#Last line