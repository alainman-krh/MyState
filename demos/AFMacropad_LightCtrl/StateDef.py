#demos\AFMacropad_LightCtrl\StateDef.py
#-------------------------------------------------------------------------------
from MyState.FieldPresets import BFLD_Toggle, BFLD_Percent_Int, BGRP_RGB
from MyState.Main import StateBlock, ListenerRoot

STATEBLK_CFG = StateBlock("CFG", [
    #Full white for now (overwritten by config_reset.state!):
	BGRP_RGB("kitchen", dflt=(255,255,255)),
	BGRP_RGB("livingroom", dflt=(255,255,255)),
	BGRP_RGB("garage", dflt=(255,255,255)),
	BGRP_RGB("bedroom1", dflt=(255,255,255)),
	BGRP_RGB("bedroom2", dflt=(255,255,255)),
	BGRP_RGB("bedroom3", dflt=(255,255,255)),
])
STATEBLK_MAIN = StateBlock("Main", [
	BFLD_Toggle("kitchen.enabled", dflt=1),
	BFLD_Percent_Int("kitchen.level", dflt=100),
	BFLD_Toggle("livingroom.enabled", dflt=1),
	BFLD_Percent_Int("livingroom.level", dflt=100),
	BFLD_Toggle("garage.enabled", dflt=1),
	BFLD_Percent_Int("garage.level", dflt=100),

	BFLD_Toggle("bedroom1.enabled", dflt=1),
	BFLD_Percent_Int("bedroom1.level", dflt=100),
	BFLD_Toggle("bedroom2.enabled", dflt=1),
	BFLD_Percent_Int("bedroom2.level", dflt=100),
	BFLD_Toggle("bedroom3.enabled", dflt=1),
	BFLD_Percent_Int("bedroom3.level", dflt=100),
])

#Signal entry point for anything wanting to control this device (ex: PC/other uController, ...):
MYSTATE = ListenerRoot([STATEBLK_CFG, STATEBLK_MAIN])

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