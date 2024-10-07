#demos\TestSerial_AFMacropad\main.py
#-------------------------------------------------------------------------------
import time
import board
import busio

r"""DESCRIPTION:
- Transmits a message to TestSerial_RP2040.
"""

MSG = "message\n"

TX = board.SDA; RX = board.SCL
uart = busio.UART(TX, RX, baudrate=115200)

print("hello")
while True:
    print(MSG)
    uart.write(MSG)
    time.sleep(2)
