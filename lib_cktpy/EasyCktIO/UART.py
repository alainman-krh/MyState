#EasyCktIO/UART.py: Tools to communicate more easily using UART.
#-------------------------------------------------------------------------------
from MyState.SigTools import SignalListenerIF
from MyState.SigIO import SigIOController
from MyState.CtrlInputs.Timebase import now_ms
import busio

r"""REF:
- <https://learn.adafruit.com/circuitpython-essentials/circuitpython-uart-serial>

Standard serial baud rates:
- 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600
"""


#==SigIO_UART
#===============================================================================
class SigIO_UART(SigIOController):
	"""Read a script from a string"""
	def __init__(self, listener:SignalListenerIF, uart:busio.UART, timeoutms_sigio=1_000):
		super().__init__(listener)
		self.uart = uart
		#self.uart.timeout=0 ??
		self.timeoutms_sigio = timeoutms_sigio

#Implement SigIOIF interface:
#-------------------------------------------------------------------------------
	def readline_noblock(self):
		return self.uart.readline() #non-blocking

	def readline_block(self):
		#Doesn't completely block. Can fail (return: None) - but will not immediately return.
		tstart = now_ms()
		while True:
			line = self.uart.readline()
			if line != None:
				return line
			twait = now_ms() - tstart
			if twait >= self.timeoutms_sigio:
				return None

	def write(self, msgstr):
		self.uart.write(msgstr)