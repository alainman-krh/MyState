#demos\LightCtrl3Boards_2040pico\main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #Defines device state
#from MyState.SigTools import SignalListenerIF
from EasyCktIO.USBSerial import SigLink_USBHost
from EasyCktIO.UART import SigCom_UART
from MyState.Signals import SigEvent
from StateReact import MainStateSync, SenseFilter
import board, busio
import os


#==Main configuration
#===============================================================================
#Common baud rates: 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600
BAUDRATE_MACROPAD = 115200 #Talking to macropad
SIGBUFSZ_RX = 128 #Buffer size for recieving MyState "signals". Should be sufficient for a few signals without overflowing
USEOPT_ROTENCODERS = True #Disable if no NeoRotary 4 connected through I2C.
MAP_LIGHTINDEX = { #Mapping for {light index => id_area} (See: StateDef.STATEBLK_MAIN for id_area)
	0: "kitchen", 1: "livingroom", 2: "garage",
	3: "bedroom1", 4: "bedroom2", 5: "bedroom3",
}
FILEPATH_CONFIG = "config_reset.state" #User can set initial state here (list of "SET" commands)
TX_MACROPAD = board.GP12; RX_MACROPAD = board.GP13


#==Global declarations
#===============================================================================
LINK_USBHOST = SigLink_USBHost(MYSTATE) #Direct link to state.
UART_MACROPAD = busio.UART(TX_MACROPAD, RX_MACROPAD, baudrate=BAUDRATE_MACROPAD, receiver_buffer_size=SIGBUFSZ_RX) #Talking to MacroPad
COM_MACROPAD = SigCom_UART(UART_MACROPAD) #No direct link to state. Manually process messages.
STATE_SYNC = MainStateSync(MAP_LIGHTINDEX, [COM_MACROPAD]) #Keep macropad + bluefruit (TODO) lights in sync.
SENSE_FILT = SenseFilter(STATE_SYNC.roomcache_map)
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
print("HELLO-mainboard (LightCtrl3Boards)") #DEBUG: Change me to ensure uploaded version matches.

while True:
	LINK_USBHOST.process_signals() #Host might send signals through USB serial
	COM_MACROPAD.signalqueue_processio()
	sig = COM_MACROPAD.signalqueue_popnext() #Low event count... don't need to loop
	if SigEvent == type(sig):
		print(sig.serialize())
		from_macropad = ("MP" == sig.section)
		iskeypress = from_macropad and ("BTNPRESS" == sig.id)
		isencdelta = from_macropad and ("ENCCHANGE" == sig.id)
		if iskeypress:
			light_idx = sig.val
			SENSE_FILT.filter_keypress(light_idx)
		elif isencdelta:
			SENSE_FILT.filter_MPencoder(sig.val)
		else:
			print("Unexpected `SigEvent` from Macropad.")
	elif sig != None:
		print("Unexpected signal from Macropad.")

	#Filter external I2C encoder knobs (NeoRotary 4) - mostly to control RGB:
	if USEOPT_ROTENCODERS:
		for (i, enc) in enumerate(ENCODERS_I2C):
			delta = enc.read_delta() #Relative to last time read.
			if delta != 0:
				print(f"ENC{i}, delta:{delta}")
				SENSE_FILT.filter_I2Cencoder(i, delta)

