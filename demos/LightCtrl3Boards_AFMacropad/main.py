#demos\LightCtrl3Boards_AFMacropad\main.py
#-------------------------------------------------------------------------------
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER
from MyState.Main import StateBlock, ListenerRoot
from EasyCktIO.UART import SigCom_UART
from MyState.Signals import SigEvent
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


#==Cache of signals to send to main controller (avoid re-creating objects)
#===============================================================================
SIG_BTN_PRESS = SigEvent("KP", "BTNPRESS") #Value: Button that was pressed
SIG_ENC_CHANGE = SigEvent("KP", "ENCCHANGE") #Value: Delta of the encoder


#==Main loop
#===============================================================================
print("HELLO-Dumb macropad (LightCtrl3Boards)") #DEBUG: Change me to ensure uploaded version matches.

while True:
	#Filter button inputs into state control signals:
	for (idx, key) in enumerate(KP_BUTTONS):
		key:KeypadElement
		key_event = key.events.get()
		if not key_event: continue #Nothing. Check next key
		if key_event.pressed:
			SIG_BTN_PRESS.val = idx
			print("PRESS:", idx)
			COM_MAINCTRL.send_signal(SIG_BTN_PRESS) #Don't need a response

	#Filter built-in rotary encoder knob into state control signals:
	delta = KP_ENCKNOB.read_delta() #Resets position to 0 every time.
	if delta != 0:
		SIG_ENC_CHANGE.val = delta
		COM_MAINCTRL.send_signal(SIG_ENC_CHANGE) #Don't need a response
		print("CHANGE:", delta)
