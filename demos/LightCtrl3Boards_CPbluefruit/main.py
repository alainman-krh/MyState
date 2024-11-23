#demos\LightCtrl3Boards_CPbluefruit\main.py
#-------------------------------------------------------------------------------
from MyState.Signals import SigEvent, SigSet, SigUpdate
from EasyCktIO.UART import SigCom_UART
import neopixel
import board, busio


r"""ABOUT
In this configuration, the Circuit Playground acs as a "dumb" neopixel controller
receiving its state as signals from the main controller.
"""

#==Main configuration
#===============================================================================
MAX_BRIGHTNESS = 0.3 #Limit max brightness... these Neopixels are bright!!!
NUM_NEOPIXELS = 10 #Circuit playground has 10
PIN_NEOPIXEL = board.NEOPIXEL
BAUDRATE_MAINCTRL = 115200 #Talking to main controller
SIGBUFSZ_RX = 128 #Buffer size for recieving MyState "signals". Should be sufficient for a few signals without overflowing
TX_MAINCTRL = board.TX; RX_MAINCTRL = board.RX


#==Global declarations
#===============================================================================
UART_MAINCTRL = busio.UART(TX_MAINCTRL, RX_MAINCTRL, baudrate=BAUDRATE_MAINCTRL, receiver_buffer_size=SIGBUFSZ_RX) #Talking to main controller
COM_MAINCTRL = SigCom_UART(UART_MAINCTRL) #No link to state. Manually process messages.
NEOPIXELS = neopixel.NeoPixel(PIN_NEOPIXEL, NUM_NEOPIXELS, brightness=MAX_BRIGHTNESS, auto_write=False)

#==Cache of signals to send to main controller from macropad ("MP"; avoid re-creating objects)
#===============================================================================
SIG_UPDATE = SigUpdate("ROOT", val=1)


#==Main loop
#===============================================================================
print("HELLO-Dumb CPboard light controller (LightCtrl3Boards)") #DEBUG: Change me to ensure uploaded version matches.
COM_MAINCTRL.send_signal(SIG_UPDATE)
NEOPIXELS[0] = (255, 0, 0)
NEOPIXELS.show() #Send updated color values to actual neopixels

while True:
	#Update Neopixels:
	COM_MAINCTRL.signalqueue_processio()
	pixels_updated = False
	while not COM_MAINCTRL.signalqueue_isempty(): #Process all available signals
		sig = COM_MAINCTRL.signalqueue_popnext()
		if SigSet != type(sig):
			print("Unknown signal:", sig.serialize())
			continue

		sig:SigSet
		idx = None
		#print(sig.serialize())
		from_mainctrl = ("Main" == sig.section)
		islightsig = from_mainctrl and ("light" == sig.id[:5])
		if islightsig:
			try:
				idx = int(sig.id[5:])
			except:
				pass #
		#Update/set specified light value:
		if idx in range(len(NEOPIXELS)):
			#print(idx, f"0x{sig.val:08X}")
			NEOPIXELS[idx] = sig.val
			pixels_updated = True

	if pixels_updated:
		NEOPIXELS.show() #Send updated color values to actual neopixels

#Last line