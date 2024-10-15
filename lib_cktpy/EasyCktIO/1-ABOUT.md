## `EasyCktIO`
<!----------------------------------------------------------------------------->
Simplified interaction with buttons, rotary encoders, and other sensors/input devices.

# `EasyCktIO.digitalio`
<!----------------------------------------------------------------------------->
Simplified interface to buttons sensed using `digitalio`.

# `EasyCktIO.adafruit_neokey`
<!----------------------------------------------------------------------------->
Simplified interface to `EasyNeoKey_1x4` using `EasyButton`/`ButtonSensorIF`.

# `EasyCktIO.USBHID_Keyboard`
<!----------------------------------------------------------------------------->
Simplified interface to `adafruit_hid`: keyboard/consumer_control
Example:
```python
from EasyCktIO.USBHID_Keyboard import KeysMain, KeysCC, Keycode, CCC
from time import sleep

key1 = KeysMain(Keycode.KEYPAD_ENTER) #Object that sends keypad "enter" code
key1.press(); sleep(0.1); key1.release()

key2 = KeysCC(CCC.MUTE) #Object that sends multimedia "mute" code
key2.press(); sleep(0.1); key2.release()
```

### Resources
- <https://docs.circuitpython.org/projects/hid/en/latest/index.html>
