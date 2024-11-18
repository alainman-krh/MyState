#demos\LightCtrl3Boards_AFMacropad\main.py
#-------------------------------------------------------------------------------
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER
from MyState.Main import StateBlock, ListenerRoot
from EasyCktIO.UART import SigIO_UART
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
TX = board.SDA; RX = board.SCL #Blue/Yellow on STEMMA-QT port


#==Global declarations
#===============================================================================
UART_CTRL = busio.UART(TX, RX, baudrate=9600) #115200 #Talks to controller
UART_SIGIO = SigIO_UART(UART_CTRL)
KP_BUTTONS = [KeypadElement(idx=i) for i in range(12)]
KP_ENCKNOB = KEYPAD_ENCODER #Alias


#==Cache of signals to send to main controller (avoid re-creating objects)
#===============================================================================
SIG_BTN_PRESS = SigEvent("KP", "BTNPRESS", 0) #Value: Button that was pressed
SIG_ENC_CHANGE = SigEvent("KP", "ENCCHANGE", 0) #Value: Delta of the encoder


#==Main loop
#===============================================================================
print("HELLO-Dumb macropad (LightCtrl3Boards)") #DEBUG: Change me to ensure uploaded version matches.

while True:
	#Filter button inputs into state control signals:
	for (idx, key) in enumerate(KP_BUTTONS):
		key:KeypadElement
		key_event = key.events.get()
		if key_event:
			if key_event.pressed:
				SIG_BTN_PRESS.val = idx
				UART_SIGIO.send_signal(SIG_BTN_PRESS)
				print("PRESS:", idx)

	#Filter built-in rotary encoder knob into state control signals:
	delta = KP_ENCKNOB.read_delta() #Resets position to 0 every time.
	if delta != 0:
		SIG_ENC_CHANGE.val = delta
		UART_SIGIO.send_signal(SIG_ENC_CHANGE)
		print("CHANGE:", delta)
