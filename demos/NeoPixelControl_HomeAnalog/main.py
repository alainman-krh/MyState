#demos\NeoPixelControl_HomeAnalog\Main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #To initialize settings
from PhyController import RefreshAgent, PHYSTATE
from HAL_Macropad import KeypadElement, IncrEncoderSensor, KEYPAD_ENCODER
from MyState.Predefined.RotEncoders import EasyEncoder_Signal
from MyState.Signals import SigSet


#==Main configuration
#===============================================================================
KPSWITCHES = {
	"kitchen": KeypadElement(0, "kitchen", PHYSTATE, "KP"),
	"room1": KeypadElement(1, "room1", PHYSTATE, "KP"),
}
#Context dependent. SigIncrement will be changed:
KPKNOB = EasyEncoder_Signal("KPenc",
	IncrEncoderSensor(KEYPAD_ENCODER, scale=5), PHYSTATE, "KP"
)


#==Global declarations
#===============================================================================
ragent = RefreshAgent(KPSWITCHES)


#==Main code entry
#===============================================================================
print("HELLO12")
MYSTATE.signal_process(SigSet("Main", "kitchen.level", 5))
MYSTATE.signal_process(SigSet("Main", "room1.level", 100))
while True:
	for sw in KPSWITCHES.values():
		sw.btn.process_inputs()
	KPKNOB.process_inputs()
