#demos\LightCtrlMP_PCcontrol\Test_MyState.py
#-------------------------------------------------------------------------------
from serial import Serial

com = Serial("COM16")

com.write("DMP ROOT".encode("ascii"))

for lines in com.readlines():
	print(lines)