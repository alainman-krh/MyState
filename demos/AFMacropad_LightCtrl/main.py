#demos\AFMacropad_LightCtrl\main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #To initialize settings
from IFaceDef_Macropad import PhyController
from MyState.Signals import SigSet, SigUpdate
import os


#==Main configuration
#===============================================================================
KPMAP_SWITCHES = { #Mapping for {btnidx => area} (See: StateDef.STATEBLK_MAIN)
	0: "kitchen", 1: "room1",
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
print("HELLO21") #DEBUG: Change me to ensure uploaded version matches.
while True:
	CTRLPAD.process_inputs()
