#demos\NeoPixelControl_HomeAnalog\Main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #To initialize settings
from PhyController import RefreshAgent, PHYSTATE
from HAL_Macropad import KeypadElement, EncoderSense, KEYPAD_ENCODER
from MyState.Predefined.RotEncoders import EasyEncoder_Incr
from MyState.Signals import SigSet, SigGet, SigIncrement


#==Main configuration
#===============================================================================
KPSWITCHES = {
	"kitchen": KeypadElement(0, "kitchen", PHYSTATE, "KP"),
	"room1": KeypadElement(1, "room1", PHYSTATE, "KP"),
}
#Context dependent. SigIncrement will be changed:
KPKNOB = EncoderSense(KEYPAD_ENCODER,
	#TODO: Find a way to scale by 1 when pressing down
	EasyEncoder_Incr(MYSTATE, SigIncrement("Main", "kitchen.level", 0)), scale = 5
)
#KPKNOB = EncoderSense(KEYPAD_ENCODER, EasyEncoder_Incr(MYSTATE, SigIncrement("Main", "NOCONN")))


#==Global declarations
#===============================================================================
ragent = RefreshAgent(KPSWITCHES)


#==Main code entry
#===============================================================================
print("HELLO10")
MYSTATE.signal_process(SigSet("Main", "kitchen.level", 5))
MYSTATE.signal_process(SigSet("Main", "room1.level", 100))
while True:
	for sw in KPSWITCHES.values():
		sw.btn.process_inputs()
	KPKNOB.handler.process_withinputs(KPKNOB.pos_getdelta())
