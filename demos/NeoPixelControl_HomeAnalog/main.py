#demos\NeoPixelControl_HomeAnalog\main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #To initialize settings
from PhyController import PhyController
from MyState.Signals import SigSet


#==Main configuration
#===============================================================================
KPMAP_SWITCHES = { #Mapping for {btnidx => area} (See: StateDef.STATEBLK_MAIN)
	0: "kitchen", 1: "room1",
}


#==Global declarations
#===============================================================================
CTRLPAD = PhyController(KPMAP_SWITCHES)


#==Main code entry
#===============================================================================
print("HELLO23")
#Pre-configure state:
MYSTATE.process_signal(SigSet("Main", "kitchen.level", 5))
MYSTATE.process_signal(SigSet("Main", "room1.level", 100))

while True:
	CTRLPAD.process_inputs()
