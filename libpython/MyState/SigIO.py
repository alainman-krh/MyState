#MyState/SigIO.py
#-------------------------------------------------------------------------------

#==SigIOIF
#===============================================================================
class SigIOIF:
	r"""Standard way to interface with IO com channels used for signalling
	(Split out from SigIOController for readability purposes)
	"""
	#@abstractmethod #Doesn't exist
	def readline_noblock(self):
		#Expect: return none if data not yet available
		pass

	def readline_block(self):
		#Expect: return none if data not yet available
		pass

	def write(self):
		pass


#==SigIOController
#===============================================================================
class SigIOController(SigIOIF):
	def __init__(self):
		return