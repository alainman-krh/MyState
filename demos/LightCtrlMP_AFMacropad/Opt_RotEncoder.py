#demos\LightCtrlMP_AFMacropad\Opt_RotEncoder.py
#-------------------------------------------------------------------------------
from CtrlInputWrap.rotaryio import EncoderSensorRIO
from adafruit_seesaw.rotaryio import IncrementalEncoder as IEncoder
import adafruit_seesaw.neopixel
import adafruit_seesaw.digitalio
from adafruit_seesaw.seesaw import Seesaw
import board

r"""NOTE/OPTIONAL:
- Can add this module to control LED colors using rotary encoder

"""

#==Constants
#===============================================================================
#Access to I2C/seesaw
SEESAW_ADDR = 0x49 #Seesaw on rot encoder (default: 0x49)
I2C = board.STEMMA_I2C()
SEESAW = Seesaw(I2C, SEESAW_ADDR)

ENCODERS_I2C = [EncoderSensorRIO(IEncoder(SEESAW, n), scale=5) for n in range(4)]