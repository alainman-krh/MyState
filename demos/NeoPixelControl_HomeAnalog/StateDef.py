#demos\NeoPixelControl_HomeAnalog\StateDef.py
#-------------------------------------------------------------------------------
from MyState.Main import StateRoot, StateBlock
from MyState.FieldPresets import BFLD_Toggle, BFLD_Percent_Int, BGRP_RGB
from MyState.SigTools import SignalListenerIF
from MyState.Signals import SigAbstract, SigDirect, SigToggle

STATEBLK_CFG = StateBlock("CFG", [
	BGRP_RGB("kitchen", dflt=(255,255,255)),
	BGRP_RGB("room1", dflt=(255,255,255)),
])
STATEBLK_MAIN = StateBlock("Main", [
	BFLD_Toggle("kitchen.enabled"),
	BFLD_Percent_Int("kitchen.level"),
	BFLD_Toggle("room1.enabled"),
	BFLD_Percent_Int("room1.level"),
])

MYSTATE = StateRoot([STATEBLK_CFG, STATEBLK_MAIN])

class PhyController(SignalListenerIF): #In charge of physical interface
	def __init__(self):
		self.active_area = "NoneYet"
		self.sig_lighttoggle = { #Cache signal objects
			"kitchen": SigToggle("Main", "kitchen.enabled"),
			"room1": SigToggle("Main", "room1.enabled"),
		}

	def signal_process(self, sig:SigAbstract):
		if "press_kitchen" == sig.id:
			self.active_area = "kitchen"
			MYSTATE.signal_process(self.sig_lighttoggle["kitchen"])
		elif "press_room1" == sig.id:
			self.active_area = "room1"
			MYSTATE.signal_process(self.sig_lighttoggle["room1"])
PHYCTRL = PhyController()


sigstr = """
SET CFG:kitchen.(R,G,B) (240,180,0)
SET Main:kitchen.enabled 1
SET Main:kitchen.level 75
INC Main:kitchen.level -5
TOG Main:kitchen.level
UPD Main
GET CFG:room1.(R,G,B)
GET CFG:kitchen.(R,G,B)
"""