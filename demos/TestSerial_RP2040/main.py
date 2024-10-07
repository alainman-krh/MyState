#demos\TestSerial_RP2040\main.py
#-------------------------------------------------------------------------------
import time
import board
import busio


r"""DESCRIPTION:
- Prints message sent from TestSerial_AFMacropad.
"""


TX = board.GP8; RX = board.GP9
uart = busio.UART(TX, RX, baudrate=115200)#, timeout=0.001)

print("hello")
while True:
    line = uart.readline()
    if line != None:
        print(line)
