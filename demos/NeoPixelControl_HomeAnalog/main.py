#demos\NeoPixelControl_HomeAnalog\Main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #To initialize settings
from PhyController import RefreshAgent, PHYSTATE
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER
from CtrlInputWrap.RotEncoders import EncoderSensorRIO
from MyState.Predefined.RotEncoders import EasyEncoder_Signal
from MyState.Signals import SigSet


#==Main configuration
#===============================================================================
KPSWITCHES = {
	"kitchen": KeypadElement(PHYSTATE, "KP", "kitchen", idx=0),
	"room1": KeypadElement(PHYSTATE, "KP", "room1", idx=1),
}
KPKNOB = EasyEncoder_Signal(PHYSTATE, "KP", "KPenc", KEYPAD_ENCODER)


#==Global declarations
#===============================================================================
ragent = RefreshAgent(KPSWITCHES)


#==Main code entry
#===============================================================================
print("HELLO21")
MYSTATE.signal_process(SigSet("Main", "kitchen.level", 5))
MYSTATE.signal_process(SigSet("Main", "room1.level", 100))
while True:
	for sw in KPSWITCHES.values():
		sw.btn.process_inputs()
	KPKNOB.process_inputs()
