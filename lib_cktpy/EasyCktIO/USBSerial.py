#EasyCktIO/USBSerial.py: Tools to access serial over USB more easily
#-------------------------------------------------------------------------------
from MyState.SigTools import SignalAwareStateIF
from MyState.SigIO import SigIOIF, SigCom, SigLink
from usb_cdc import console as HOSTSERIAL_IN
from array import array
from sys import stdin, stdout

r"""ASSUMPTIONS:
- stdin, stdout are USB-serial input/output streams (not necessarily true).
"""


#==USBSerialIn_Nonblocking
#===============================================================================
class USBSerialIn_Nonblocking():
	def __init__(self, szbuf=500):
		HOSTSERIAL_IN.timeout=0
		self.linebuf = []
		self.buf = array("b", [0]*szbuf)
		self.reset_buf()
	def reset_buf(self):
		self.pos = 0

	def buf_append(self, bufin:bytes):
		char_break = (ord("\n"), ord("\r"))
		szbuf = len(self.buf)
		posbuf = self.pos
		szin = len(bufin)
		posin = 0
		newchar = ""

		while posin < szin:
			while szbuf >= posbuf:
				if posin >= szin: break
				newchar = bufin[posin]
				self.buf[posbuf] = newchar
				posbuf+=1; posin+=1
				if newchar in char_break: break
			if (newchar in char_break) or (posbuf >= szbuf):
				line = bytes(self.buf[:posbuf]).decode("utf-8")
				self.linebuf.append(line)
				posbuf = 0 #Reset buffer
		self.pos = posbuf

	def readline(self):
		bufin = HOSTSERIAL_IN.readline()
		if len(bufin) > 0:
			self.buf_append(bufin)
		if len(self.linebuf) > 0:
			return self.linebuf.pop(0) #Not super efficient.
		return None


#==SigIO_USBHost/SigCom_USBHost/SigLink_USBHost
#===============================================================================
class SigIO_USBHost(SigIOIF):
	"""Implement SigIOIF interface for a USB host device"""
	def __init__(self):
		self.istream_nonblock = USBSerialIn_Nonblocking()

#Implement SigIOIF interface:
#-------------------------------------------------------------------------------
	def readline_noblock(self):
		return self.istream_nonblock.readline()

	def readline_block(self):
		return stdin.readline()

	def write(self, msgstr):
		stdout.write(msgstr)


#Convenience constructors
#-------------------------------------------------------------------------------
def SigCom_USBHost():
	io = SigIO_USBHost()
	return SigCom(io)
def SigLink_USBHost(state:SignalAwareStateIF):
	io = SigIO_USBHost()
	return SigLink(io, state)
