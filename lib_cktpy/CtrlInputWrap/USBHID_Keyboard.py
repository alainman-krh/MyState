#CtrlInputWrap/USBHID_Keyboard.py: Simplified interface to adafruit_hid: keyboard/consumer_control
#-------------------------------------------------------------------------------
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode as CCC #Convenience for module user
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode #Convenience for module user
import usb_hid


#=Resources
#===============================================================================
#https://docs.circuitpython.org/projects/hid/en/latest/index.html


#=Constants
#===============================================================================
#Access to standard HID/Keyboard & HID/ConsumerControl (No need for user to construct directly):
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)


#=Classes
#===============================================================================
class KeyCombination: #Simplified, common interface for sending key combinations (HID/Keyboard & HID/ConsumerControl)
    def __init__(self, dev, keycodes, release_has_args=True) -> None:
        self.dev = dev
        if type(keycodes) is int:
            keycodes = (keycodes,) #Make tuple
        self.keycodes = keycodes

        keycodes_release = keycodes
        if not release_has_args:
            keycodes_release = tuple() #No args
        self.keycodes_release = keycodes_release
    def press(self):
        self.dev.press(*self.keycodes)
    def release(self):
        self.dev.release(*self.keycodes_release)


#=Convenience/constructor functions
#===============================================================================
def KeysMain(keycodes):
    return KeyCombination(kbd, keycodes)
def KeysCC(keycodes):
    return KeyCombination(cc, keycodes, release_has_args=False)

#Last line