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
	def __init__(self, uart:busio.UART, listener:SignalListenerIF=None, timeoutms_sigio=1_000):
		super().__init__(listener)
		self.uart = uart
		self.uart.timeout = 0 #Is it wise to change it?? Should we just create UART directly?
		self.timeoutms_sigio = timeoutms_sigio

#Implement SigIOIF interface:
#-------------------------------------------------------------------------------
	def readline_noblock(self):
		line_bytes = self.uart.readline() #non-blocking
		if line_bytes is None:
			return None
		return line_bytes.decode("utf-8")

	def readline_block(self):
		#Doesn't completely block. Can fail (return: None) - but will not immediately return.
		tstart = now_ms()
		while True:
			line_bytes = self.uart.readline() #non-blocking
			if line_bytes != None:
				return line_bytes.decode("utf-8")
			twait = now_ms() - tstart
			if twait >= self.timeoutms_sigio:
				return None

	def write(self, msgstr):
		self.uart.write(msgstr.encode("utf-8"))
