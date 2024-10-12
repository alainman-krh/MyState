#demos\AFMacropad_LightCtrl\main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #To initialize settings
from IFaceDef_Macropad import PhyController
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER
import os


#==Main configuration
#===============================================================================
KPMAP_SWITCHES = { #Mapping for {btnidx => area} (See: StateDef.STATEBLK_MAIN)
	0: "kitchen", 1: "livingroom", 2: "garage",
	3: "bedroom1", 4: "bedroom2", 5: "bedroom3",
}
FILEPATH_CONFIG = "config_reset.state" #User can set initial state here (list of "SET" commands)


#==Global declarations
#===============================================================================
CTRLPAD = PhyController(KPMAP_SWITCHES)


#==Configuration before main loop
#===============================================================================
if FILEPATH_CONFIG in os.listdir("/"):
	print("Loading user defaults...", end="")
	MYSTATE.script_load(FILEPATH_CONFIG)
	print("Done.")


#==Main loop
#===============================================================================
print("HELLO24") #DEBUG: Change me to ensure uploaded version matches.
while True:
	#Process button inputs:
	for (id_area, key) in CTRLPAD.keymap.items():
		key:KeypadElement
		key_event = key.events.get()
		if key_event:
			if key_event.pressed:
				CTRLPAD.process_key(id_area)

	delta = CTRLPAD.encknob.read_delta() #Resets position to 0 every time.
	if delta != 0:
		CTRLPAD.process_KPencoder(delta)
