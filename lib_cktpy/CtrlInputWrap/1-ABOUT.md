## `CtrlInputWrap`
<!----------------------------------------------------------------------------->
Simplified interaction with buttons, rotary encoders, and other sensors/input devices.

# `CtrlInputWrap.Buttons`
<!----------------------------------------------------------------------------->
State machine (FSM) controlling interations various types of buttons.
- `CtrlInputWrap.Buttons.EasyNeoKey_1x4`: Interacting with NeoKey 1x4 keypad.
- TODO: Add more!

# `CtrlInputWrap.USBHID_Keyboard`
<!----------------------------------------------------------------------------->
Simplified interface to adafruit_hid: keyboard/consumer_control
Example:
```python
from CtrlInputWrap.USBHID_Keyboard import KeysMain, KeysCC, Keycode, CCC
from time import sleep

key1 = KeysMain(Keycode.KEYPAD_ENTER) #Object that sends keypad "enter" code
key1.press(); sleep(0.1); key1.release()

key2 = KeysCC(CCC.MUTE) #Object that sends multimedia "mute" code
key2.press(); sleep(0.1); key2.release()
```

### Resources
- <https://docs.circuitpython.org/projects/hid/en/latest/index.html>
