#MyState/Signals.py
#-------------------------------------------------------------------------------

MSG_SIGACK = "ACK" #For blocking transmissions (if not returning SigValue)


#==Signal classes: Base
#===============================================================================
class SigAbstract:
	#.TYPE must be defined by concrete type
	def __init__(self, section, id="", val=0):
		#Ensure all 4 parameters can be used to construct
		self.section = section
		self.id = id
		self.val = val

	#@abstractmethod #Doesn't exist
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id}"


#==Signal classes: Concrete
#===============================================================================
class SigEvent(SigAbstract): #Generic signal for an event
	TYPE = "SIG"
class SigValue(SigAbstract):
	TYPE = "SVL"
	def __init__(self, section, id, val):
		#id & val: not optional!
		super().__init__(section, id, val)
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id} {self.val}"
class SigSet(SigAbstract):
	TYPE = "SET"
	def __init__(self, section, id, val):
		#id & val: not optional!
		super().__init__(section, id, val)
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id} {self.val}"
class SigGet(SigAbstract):
	TYPE = "GET"
class SigIncrement(SigAbstract): #Increment
	TYPE = "INC"
	def __init__(self, section, id, val):
		#id & val: not optional!
		super().__init__(section, id, val)
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id} {self.val}"
class SigToggle(SigAbstract):
	TYPE = "TOG"
#TODO: Have update disable
class SigUpdate(SigAbstract):
	TYPE = "UPD"

SIG_ALL = (SigEvent, SigValue, SigSet, SigGet, SigIncrement, SigToggle, SigUpdate)