## MyState/demos
<!----------------------------------------------------------------------------->

# Projects:
<!----------------------------------------------------------------------------->

## LightCtrl3Boards
Pretend to do light control (home automation) using 3 dev boards:
- Adafruit MacroPad (ADA-5128), RPi 2040 Pico (ADA-4864), Circuit Playground Bluefruit (ADA-764)

Files:
- `LightCtrl3Boards_2040pico/*`: Project files targeting RP2040 pico (main controller).
- `LightCtrl3Boards_2040pico/pydrv_install.toml`: What to copy to the microcontroller USB drive.
- `LightCtrl3Boards_AFMacropad/*`: Project files targeting AF-MacroPad (keypad control).
- `LightCtrl3Boards_AFMacropad/pydrv_install.toml`: What to copy to the microcontroller USB drive.
- `LightCtrl3Boards_CPbluefruit/*`: Project files targeting Circuit Playground device (emulates home lighting).
- `LightCtrl3Boards_CPbluefruit/pydrv_install.toml`: What to copy to the microcontroller USB drive.

## LightCtrlMP
Pretend to do light control (home automation) using Adafruit MacroPad (ADA-5128).
Lights represented by the keypad NeoPixels.
- `LightCtrlMP_AFMacropad/*`: Project files targeting AF-MacroPad itself.
- `LightCtrlMP_AFMacropad/pydrv_install.toml`: What to copy to the microcontroller USB drive.
