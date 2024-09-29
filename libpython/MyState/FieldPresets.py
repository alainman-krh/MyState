#MyState/FieldPresets.py
#-------------------------------------------------------------------------------
from .Primitives import StateField_Int, FieldGroup


#==Convenience constructors to build fields (BFLD_*) or build groups (BGRP_*)
#===============================================================================

def BFLD_Toggle(id, dflt=0):
	"""2 state field (1/0) that supports toggling ("TOG" signal)"""
	return StateField_Int(id, 0, 1, dflt=dflt)

def BFLD_Percent_Int(id, dflt=0):
	"""Integer between 0 and 100"""
	return StateField_Int(id, 0, 100, dflt=dflt)

def BGRP_RGB(id, dflt=(0,0,0)):
	return FieldGroup(id, (
		StateField_Int("R", 0, 255, dflt=dflt[0]),
		StateField_Int("G", 0, 255, dflt=dflt[1]),
		StateField_Int("B", 0, 255, dflt=dflt[2]),
	))