#demos\LightCtrl3Boards_2040pico\StateDef.py
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
	BGRP_RGB("hallway1", dflt=(255,255,255)),
	BGRP_RGB("hallway2", dflt=(255,255,255)),
	BGRP_RGB("hallway3", dflt=(255,255,255)),
	BGRP_RGB("basement", dflt=(255,255,255)),
	BGRP_RGB("mechroom", dflt=(255,255,255)),
	BGRP_RGB("mainentrance", dflt=(255,255,255)),
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

	BFLD_Toggle("hallway1.enabled", dflt=1),
	BFLD_Percent_Int("hallway1.level", dflt=100),
	BFLD_Toggle("hallway2.enabled", dflt=1),
	BFLD_Percent_Int("hallway2.level", dflt=100),
	BFLD_Toggle("hallway3.enabled", dflt=1),
	BFLD_Percent_Int("hallway3.level", dflt=100),

	BFLD_Toggle("basement.enabled", dflt=1),
	BFLD_Percent_Int("basement.level", dflt=100),
	BFLD_Toggle("mechroom.enabled", dflt=1),
	BFLD_Percent_Int("mechroom.level", dflt=100),
	BFLD_Toggle("mainentrance.enabled", dflt=1),
	BFLD_Percent_Int("mainentrance.level", dflt=100),
])

#Signal entry point for anything wanting to control this device (ex: PC/other uController, ...):
MYSTATE = ListenerRoot([STATEBLK_CFG, STATEBLK_MAIN])
