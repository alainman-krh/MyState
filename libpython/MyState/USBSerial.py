#MyState/USBSerial.py: Tools to access serial over USB more easily
#-------------------------------------------------------------------------------
from usb_cdc import console as HOSTSERIAL_IN
from array import array


#==USBSerialIn_Nonblocking
#===============================================================================
class USBSerialIn_Nonblocking():
	def __init__(self, szbuf=50):
		HOSTSERIAL_IN.timeout=0
		self.linebuf = []
		self.buf = array("b", [0]*szbuf)
		self.reset_buf()
	def reset_buf(self):
		self.pos = 0

	def buf_append(self, bufin):
		char_break = (ord("\n"), ord("\r"))
		szbuf = len(self.buf)
		posbuf = self.pos
		szin = len(bufin)
		posin = 0
		newchar = ""

		while posin < szin:
			while szbuf >= posbuf:
				if posin >= szin: break
				newchar = ord(bufin[posin])
				self.buf[posbuf] = newchar
				posbuf+=1; posin+=1
				if newchar in char_break: break
			if (newchar in char_break) or (posbuf >= szbuf):
				line = bytes(self.buf[:posbuf]).decode("ascii")
				self.linebuf.append(line)
				posbuf = 0 #Reset buffer
		self.pos = posbuf

	def readline(self):
		bufin = HOSTSERIAL_IN.readline().decode("ascii")
		if len(bufin) > 0:
			self.buf_append(bufin)
		if len(self.linebuf) > 0:
			return self.linebuf.pop(0) #Not super efficient.
		return None
