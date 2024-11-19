#MyState/Signals.py
#-------------------------------------------------------------------------------


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
		return f"{self.TYPE} {self.section}:{self.id} {self.val}"

class SigAbstract_wVal(SigAbstract):
	def __init__(self, section, id, val):
		super().__init__(section, id, val)

class SigAbstract_NoVal(SigAbstract):
	def __init__(self, section, id=""):
		super().__init__(section, id)

	#@abstractmethod #Doesn't exist
	def serialize(self):
		return f"{self.TYPE} {self.section}:{self.id}"


#==Signal classes: Concrete
#===============================================================================
class SigEvent(SigAbstract_wVal): #Generic signal for an event
	TYPE = "SIG"
	def __init__(self, section, id, val=0):
		#id: not optional!
		super().__init__(section, id, val)
class SigValue(SigAbstract_wVal):
	TYPE = "SVL"
	def __init__(self, section, id, val):
		#id & val: not optional!
		super().__init__(section, id, val)
class SigSet(SigAbstract_wVal):
	TYPE = "SET"
	def __init__(self, section, id, val):
		#id & val: not optional!
		super().__init__(section, id, val)
class SigGet(SigAbstract_NoVal):
	TYPE = "GET"
class SigIncrement(SigAbstract_wVal): #Increment
	TYPE = "INC"
	def __init__(self, section, id, val):
		#id & val: not optional!
		super().__init__(section, id, val)
class SigToggle(SigAbstract_NoVal):
	TYPE = "TOG"
#TODO: Have update disable
class SigUpdate(SigAbstract_wVal):
	TYPE = "UPD"
	def __init__(self, section, id="", val=1):
		#val=1: update. val=2: auto-update. val=0: disable auto-update.
		super().__init__(section, id, val)
class SigDump(SigAbstract_NoVal):
	"""Dump state ("DMP ROOT": dumps all)"""
	TYPE = "DMP"
	def serialize(self):
		return f"{self.TYPE} {self.section}"

SIG_ALL = (SigEvent, SigValue, SigSet, SigGet, SigIncrement, SigToggle, SigUpdate, SigDump)