#MyState/Signals.py
#-------------------------------------------------------------------------------


#==
#===============================================================================
class IOChanIF: #TODO:SigChanIF???
	r"""Standard way to interface with IO com channels used for signalling"""
	pass


#==Signal classes: Base
#===============================================================================
class SigAbstract:
	#.TYPE must be defined by concrete type
	def __init__(self, section, id="", val=0, iochan:IOChanIF=None):
		#Ensure all 4 parameters can be used to construct
		self.section = section
		self.id = id
		self.val = val
		self.iochan = iochan

	#@abstractmethod #Doesn't exist
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id}"


#==Signal classes: Concrete
#===============================================================================
class SigDirect(SigAbstract): #A plain signal
	TYPE = "SIG"
class SigSet(SigAbstract):
	TYPE = "SET"
	def __init__(self, section, id, val, iochan:IOChanIF=None):
		#id & val: not optional!
		super().__init__(section, id, val, iochan)
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id} {self.val}"
class SigGet(SigAbstract):
	TYPE = "GET"
class SigIncrement(SigAbstract): #Increment
	TYPE = "INC"
	def __init__(self, section, id, val, iochan:IOChanIF=None):
		#id & val: not optional!
		super().__init__(section, id, val, iochan)
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id} {self.val}"
class SigToggle(SigAbstract):
	TYPE = "TOG"
class SigUpdate(SigAbstract):
	TYPE = "UPD"

SIG_ALL = (SigSet, SigGet, SigIncrement, SigToggle, SigUpdate)