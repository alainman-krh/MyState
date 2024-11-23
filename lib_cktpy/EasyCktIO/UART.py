#EasyCktIO/UART.py: Tools to communicate more easily using UART.
#-------------------------------------------------------------------------------
from MyState.SigTools import SignalAwareStateIF
from MyState.SigIO import IOWrapIF, SigCom, SigLink
from MyState.CtrlInputs.Timebase import now_ms
import busio

r"""REF:
- <https://learn.adafruit.com/circuitpython-essentials/circuitpython-uart-serial>

Standard serial baud rates:
- 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600

# Workaround (linebuf_bytes/_readline_fix):
- uart.readline() sometimes returns "line" before end of line is actually detected.
- Observed on RP2040 devices (such as AF-Macropad). TODO: Investigate root cause.
"""


#==IOWrap_UART
#===============================================================================
class IOWrap_UART(IOWrapIF):
	"""Implement IOWrapIF interface for a UART device"""
	def __init__(self, uart:busio.UART, timeoutms_sigio=1_000):
		self.uart = uart
		self.uart.timeout = 0 #Is it wise to change it?? Should we just create UART directly?
		self.timeoutms_sigio = timeoutms_sigio
		self.linebuf_bytes = None #Workaround

#Implement IOWrapIF interface:
#-------------------------------------------------------------------------------
	def _readline_fix(self): #Workaround
		line_bytes = self.uart.readline() #non-blocking
		if line_bytes is None: return None #No change
		if len(line_bytes) < 1: return None #Not actually anything
		if self.linebuf_bytes is None:
			self.linebuf_bytes = line_bytes
		else:
			self.linebuf_bytes += line_bytes
		if b"\n" not in self.linebuf_bytes:
			return None #Still don't have a full line
		
		#Don't check to see if we have exactly one line. Assuming that's ok:
		line_bytes = self.linebuf_bytes; self.linebuf_bytes = None
		return line_bytes

	def readline_noblock(self):
		line_bytes = self._readline_fix() #non-blocking
		if line_bytes is None:
			return None
		return line_bytes.decode("utf-8")

	def readline_block(self):
		#Doesn't completely block. Can fail (return: None) - but will not immediately return.
		tstart = now_ms()
		while True:
			line_bytes = self._readline_fix() #non-blocking
			if line_bytes != None:
				return line_bytes.decode("utf-8")
			twait = now_ms() - tstart
			if twait >= self.timeoutms_sigio:
				return None

	def write(self, msgstr):
		self.uart.write(msgstr.encode("utf-8"))


#==Convenience constructors
#===============================================================================
def SigCom_UART(uart:busio.UART, timeoutms_sigio=1_000):
	io = IOWrap_UART(uart, timeoutms_sigio=timeoutms_sigio)
	return SigCom(io)
def SigLink_UART(uart:busio.UART, state:SignalAwareStateIF, timeoutms_sigio=1_000):
	io = IOWrap_UART(uart, timeoutms_sigio=timeoutms_sigio)
	return SigLink(io, state)

#Last line