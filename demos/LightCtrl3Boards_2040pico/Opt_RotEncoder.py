#demos\LightCtrl3Boards_2040pico\Opt_RotEncoder.py
#-------------------------------------------------------------------------------
from EasyCktIO.seesaw import EncoderSensorRIO, DEFAULTI2CADDR_SEESAW
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.neopixel import NeoPixel as NeoPixelSS
#import adafruit_seesaw.digitalio
import board

r"""NOTE/OPTIONAL:
- Can add this module to control LED colors using rotary encoder

"""

#==Constants
#===============================================================================
SEESAW_ADDR = DEFAULTI2CADDR_SEESAW #Seesaw on rot encoder (Assume default)
SEESAW_NEOPIXEL_PIN = 18
COLOR_RED = 0xFF0000
COLOR_GREEN = 0x00FF00
COLOR_BLUE = 0x0000FF


#==Control/objects
#===============================================================================
I2C = board.STEMMA_I2C()
SEESAW = Seesaw(I2C, SEESAW_ADDR)
ENCODERS_I2C = [EncoderSensorRIO(SEESAW, i) for i in range(4)]
NEOPIXELS_I2C = NeoPixelSS(SEESAW, SEESAW_NEOPIXEL_PIN, 4) #Under the rotary encoders

#Use neopixels to show what color components we are controlling:
NEOPIXELS_I2C.brightness = 0.5 #Not too bright
NEOPIXELS_I2C[0] = COLOR_RED
NEOPIXELS_I2C[1] = COLOR_GREEN
NEOPIXELS_I2C[2] = COLOR_BLUE

