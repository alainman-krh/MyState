#MyState/IOWrap: A more consistent interface across different IO devices
#-------------------------------------------------------------------------------

#TODO: Move to a less speficic module than `MyState`?


#==IOWrapIF
#===============================================================================
class IOWrapIF:
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


#==IOWrap_Script/SigCom_Script/SigLink_Script
#===============================================================================
class IOWrap_Script(IOWrapIF):
	"""Implement IOWrapIF from a "script" (list of "signal" strings)"""
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

#Implement IOWrapIF interface:
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