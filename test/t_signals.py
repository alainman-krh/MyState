#test/t_signals.py
#-------------------------------------------------------------------------------
from MyState.Signals import SigSet, SigGet, SigIncrement, SigToggle
from MyState.Signals import SigAbstract, SigUpdate
from MyState import SigTools

print("\nTest object construction")
#-------------------------------------------------------------------------------
sigstr = """
SET CFG:kitchen.(R,G,B) (240,180,0)
SET Main:kitchen.enabled 1
SET Main:kitchen.level 75
INC Main:kitchen.level -5
TOG Main:kitchen.level
UPD Main
GET CFG:bedroom1.(R,G,B)
GET CFG:kitchen.(R,G,B)
"""
for line in sigstr.splitlines():
	siglist = SigTools.Signal_Deserialize(line)
	for sig in siglist:
		print(sig.serialize())


print("\nTest process_signal()")

print()
#-------------------------------------------------------------------------------
from MyState.Main import ListenerRoot, StateBlock
from MyState.FieldPresets import BFLD_Toggle, BFLD_Percent_Int, BGRP_RGB

STATEBLK_CFG = StateBlock("CFG", [
	BGRP_RGB("kitchen", dflt=(255,255,255)),
	BGRP_RGB("bedroom1", dflt=(255,255,255)),
])
STATEBLK_MAIN = StateBlock("Main", [
	BFLD_Toggle("kitchen.enabled"),
	BFLD_Percent_Int("kitchen.level"),
	BFLD_Toggle("bedroom1.enabled"),
	BFLD_Percent_Int("bedroom1.level"),
])

MYSTATE = ListenerRoot([STATEBLK_CFG, STATEBLK_MAIN])

siglist = [
	SigToggle("Main", "kitchen.enabled"),
	SigSet("Main", "kitchen.level", 32),
	SigIncrement("Main", "kitchen.level", 110),
	SigGet("Main", "kitchen.level"),
	SigToggle("Main", "kitchen.enabled"),
	SigUpdate("CFG"), #This will cause something to print.
]
for sig in siglist:
	MYSTATE.process_signal(sig)