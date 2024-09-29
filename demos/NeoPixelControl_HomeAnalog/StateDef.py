#demos\NeoPixelControl_HomeAnalog\StateDef.py
#-------------------------------------------------------------------------------
from MyState.Main import StateRoot, StateBlock
from MyState.FieldPresets import BFLD_Toggle, BFLD_Percent_Int, BGRP_RGB

STATEBLK_CFG = StateBlock("CFG", [
	BGRP_RGB("kitchen", dflt=(255,255,255)),
	BGRP_RGB("room1", dflt=(255,255,255)),
])
STATEBLK_MAIN = StateBlock("Main", [
	BFLD_Toggle("kitchen.enabled"),
	BFLD_Percent_Int("kitchen.level"),
	BFLD_Toggle("room1.enabled"),
	BFLD_Percent_Int("room1.level"),
])

MYSTATE = StateRoot([STATEBLK_CFG, STATEBLK_MAIN])

sigstr = """
SET CFG:kitchen.(R,G,B) (240,180,0)
SET Main:kitchen.enabled 1
SET Main:kitchen.level 75
INC Main:kitchen.level -5
TOG Main:kitchen.level
UPD Main
GET CFG:room1.(R,G,B)
GET CFG:kitchen.(R,G,B)
"""