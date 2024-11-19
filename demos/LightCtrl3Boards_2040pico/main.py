#demos\LightCtrl3Boards_2040pico\main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #Defines device state
#from MyState.SigTools import SignalListenerIF
from EasyCktIO.USBSerial import SigLink_USBHost
from EasyCktIO.UART import SigCom_UART
from MyState.Signals import SigEvent
import board, busio
import os


#==Main configuration
#===============================================================================
#Common baud rates: 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600
BAUDRATE_MACROPAD = 115200 #Talking to macropad
SIGBUFSZ_RX = 128 #Buffer size for recieving MyState "signals". Should be sufficient for a few signals without overflowing
USEOPT_ROTENCODERS = True #Disable if no NeoRotary 4 connected through I2C.
KPMAP_SWITCHES = { #Mapping for {btnidx => area} (See: StateDef.STATEBLK_MAIN)
	0: "kitchen", 1: "livingroom", 2: "garage",
	3: "bedroom1", 4: "bedroom2", 5: "bedroom3",
}
FILEPATH_CONFIG = "config_reset.state" #User can set initial state here (list of "SET" commands)
TX_MACROPAD = board.GP12; RX_MACROPAD = board.GP13


#==Global declarations
#===============================================================================
LINK_USBHOST = SigLink_USBHost(MYSTATE) #Direct link to state.
UART_MACROPAD = busio.UART(TX_MACROPAD, RX_MACROPAD, baudrate=BAUDRATE_MACROPAD, receiver_buffer_size=SIGBUFSZ_RX) #Talking to MacroPad
COM_MACROPAD = SigCom_UART(UART_MACROPAD) #No link to state. Manually process messages.
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
	sig = COM_MACROPAD.read_signal_next()
	if SigEvent == type(sig):
		print(sig.serialize())
	elif sig != None:
		print("Unexpected signal from Macropad.")

	#Filter external I2C encoder knobs (NeoRotary 4) - mostly to control RGB:
	if USEOPT_ROTENCODERS:
		for (i, enc) in enumerate(ENCODERS_I2C):
			delta = enc.read_delta() #Relative to last time read.
			if delta != 0:
				print(f"ENC{i}, delta:{delta}")
				#CTRLPAD.filter_I2Cencoder(i, delta)

