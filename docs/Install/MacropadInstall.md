## Macropad install/upload
<!----------------------------------------------------------------------------->

# Supplementary documentation
- <https://learn.adafruit.com/adafruit-macropad-rp2040>

# Installing CircuitPython environment
Download .uf2 file here (v9.14 tested):
- <https://circuitpython.org/board/adafruit_macropad_rp2040/>

Plug in USB-C to macropad while holding the BOOTSEL button (press on rotary encoder).
- A new drive should get mounted on your system.
- Drag/drop downloaded .uf2 file onto newly mounted drive (RPI-RP2).

# Required packages
<!----------------------------------------------------------------------------->
Project `LightCtrlMP` depends on libraries included in the "CircuitPython Library Bundle"
found [HERE](https://circuitpython.org/libraries):
- `neopixel`

Optionally, "LightCtrlMP_AFMacropad" can make use of Adafruit Quad Rotary Encoder (#5752).
To get the quad encoders working (setting `USEOPT_ROTENCODERS=True`), the following
libs are also required:
- `adafruit_seesaw/`

Installing dependencies (required packages):
1. Download "Library Bundle" corresponding to your version of CircuitPython.
1. Unzip "Bundle" somewhere on your computer.
1. Copy required modules from the `lib/` subdirectory found in the resultant
   unzipped "Bundle" folder.

