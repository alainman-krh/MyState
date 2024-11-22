#demos\LightCtrl3Boards_AFMacropad\main.py
#-------------------------------------------------------------------------------
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER
from MyState.Main import StateBlock, ListenerRoot
from MyState.Signals import SigEvent, SigSet
from EasyCktIO.UART import SigCom_UART
import board, busio

r"""ABOUT
In this configuration, the macropad here is a sort of "dumb" interface that
simply relays encoder change and button press events.

On STEMMA-QT:
- Pin order is: GND (black), VCC3.3 (red), SDA (blue), SCL (yellow).
"""


#==Main configuration
#===============================================================================
BAUDRATE_MAINCTRL = 115200 #Talking to main controller
TX_MAINCTRL = board.SDA; RX_MAINCTRL = board.SCL #Blue/Yellow on STEMMA-QT port


#==Global declarations
#===============================================================================
UART_MAINCTRL = busio.UART(TX_MAINCTRL, RX_MAINCTRL, baudrate=BAUDRATE_MAINCTRL) #Talking to main controller
COM_MAINCTRL = SigCom_UART(UART_MAINCTRL) #No link to state. Manually process messages.
KP_BUTTONS = [KeypadElement(idx=i) for i in range(12)]
KP_ENCKNOB = KEYPAD_ENCODER #Alias


#==Cache of signals to send to main controller from macropad ("MP"; avoid re-creating objects)
#===============================================================================
SIG_BTN_PRESS = SigEvent("MP", "BTNPRESS") #Value: Index of button that was pressed
SIG_ENC_CHANGE = SigEvent("MP", "ENCCHANGE") #Value: Delta of the encoder


#==Main loop
#===============================================================================
print("HELLO-Dumb macropad (LightCtrl3Boards)") #DEBUG: Change me to ensure uploaded version matches.

while True:
	#Filter button inputs into state control signals:
	for (idx, key) in enumerate(KP_BUTTONS):
		key:KeypadElement
		key_event = key.events.get()
		if not key_event: continue #Nothing. Check next key in loop
		if key_event.pressed:
			SIG_BTN_PRESS.val = idx
			#print("PRESS:", idx)
			COM_MAINCTRL.send_signal(SIG_BTN_PRESS) #Don't need a response

	#Filter built-in rotary encoder knob into state control signals:
	delta = KP_ENCKNOB.read_delta() #Resets position to 0 every time.
	if delta != 0:
		SIG_ENC_CHANGE.val = delta
		COM_MAINCTRL.send_signal(SIG_ENC_CHANGE) #Don't need a response
		#print("CHANGE:", delta)

	#Update Neopixels:
	COM_MAINCTRL.signalqueue_processio()
	if not COM_MAINCTRL.signalqueue_isempty():
		print("NEWQUEUE")
	while not COM_MAINCTRL.signalqueue_isempty(): #Process all available signals
		sig = COM_MAINCTRL.signalqueue_popnext()
#		siglist = COM_MAINCTRL.cache_siglist
#		if sig !=None and siglist is None:
#			print("signal - no cache")
#		if siglist != None:
#			N = len(siglist)
#			if N > 0:
#				print("cachlen", N)
		if SigSet != type(sig):
			print("Unknown signal:", sig.serialize())
			continue

		sig:SigSet
		idx = None
		print(sig.serialize())
		from_mainctrl = ("Main" == sig.section)
		islightsig = from_mainctrl and ("light" == sig.id[:5])
		if islightsig:
			try:
				idx = int(sig.id[5:])
			except:
				pass #
		#Update/set specified light value:
		if idx in range(len(KP_BUTTONS)):
			#print(idx, f"0x{sig.val:08X}")
			neokey = KP_BUTTONS[idx]
			neokey.pixel_set(sig.val)

#Last line