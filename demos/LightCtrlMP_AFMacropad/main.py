#demos\LightCtrlMP_AFMacropad\main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #To initialize settings
from IFaceDef_Macropad import PhyController
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER
from MyState.SigIO import SigIO_USBHost
import os


#==Main configuration
#===============================================================================
USEOPT_ROTENCODERS = True
KPMAP_SWITCHES = { #Mapping for {btnidx => area} (See: StateDef.STATEBLK_MAIN)
	0: "kitchen", 1: "livingroom", 2: "garage",
	3: "bedroom1", 4: "bedroom2", 5: "bedroom3",
}
FILEPATH_CONFIG = "config_reset.state" #User can set initial state here (list of "SET" commands)


#==Global declarations
#===============================================================================
HOSTIO = SigIO_USBHost(MYSTATE)
CTRLPAD = PhyController(KPMAP_SWITCHES)
if USEOPT_ROTENCODERS:
	from Opt_RotEncoder import ENCODERS_I2C
	print("ENCODERS DETECTED")


#==Configuration before main loop
#===============================================================================
if FILEPATH_CONFIG in os.listdir("/"):
	print("Loading user defaults...", end="")
	MYSTATE.script_load(FILEPATH_CONFIG)
	print("Done.")


#==Main loop
#===============================================================================
print("HELLO22") #DEBUG: Change me to ensure uploaded version matches.
state = MYSTATE.state_getdump("ROOT")
for line in state:
	print(line)

while True:
	HOSTIO.process_signals() #Host might send signals through USB serial

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

	if USEOPT_ROTENCODERS:
		for (i, enc) in enumerate(ENCODERS_I2C):
			delta = enc.read_delta() #Relative to last time read.
			if delta != 0:
				CTRLPAD.process_I2Cencoder(i, delta)

