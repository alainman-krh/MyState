#demos\NeoPixelControl_HomeAnalog\PhyController.py
#-------------------------------------------------------------------------------
from StateDef import STATEBLK_CFG, STATEBLK_MAIN, MYSTATE, StateBlock
from MyState.Signals import SigAbstract, SigUpdate, SigToggle, SigIncrement
from MyState.SigTools import SignalListenerIF
from HAL_Macropad import KeypadElement


#==RefreshAgent: Handles refreshing device when its state updates
#===============================================================================
class RefreshAgent(SignalListenerIF):
	"""Refreshes state after it gets updated (SigUpdate)"""
	def __init__(self, switch_d):
		self.switch_d = switch_d
		for blk in (STATEBLK_CFG, STATEBLK_MAIN):
			blk:StateBlock
			blk.listener_add(self)

	def compute_color(self, id_area, color_100):
		fields_main = STATEBLK_MAIN.field_d
		scale = (fields_main[id_area + ".level"].val / 100)
		scale *= fields_main[id_area + ".enabled"].val
		return tuple(int(vi*scale) for vi in color_100)

	def update_lights(self):
		color_100 = (255,255,255) #At full brightness

		for (id_area, sw) in self.switch_d.items():
			sw:KeypadElement
			color = self.compute_color(id_area, color_100)
			sw.pixel_set(color)

	def signal_process(self, sig:SigAbstract):
		if type(sig) != SigUpdate:
			return False

		sec = None
		if "CFG" == sig.section:
			sec:StateBlock = STATEBLK_CFG
		elif "Main" == sig.section:
			sec:StateBlock = STATEBLK_MAIN
			self.update_lights()
		else:
			return False

		#Just print out for now:
		for (id, field) in sec.field_d.items():
			print(f"{id}: {field.val}")
		return True


#==PhyState: State of physical control panel (vs core device function: MYSTATE)
#===============================================================================
class PhyState(SignalListenerIF):
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
		elif "change_KPenc" == sig.id:
			ctrlid = self.active_area + ".level"
			sig = SigIncrement("Main", ctrlid, sig.val)
			MYSTATE.signal_process(sig)
PHYSTATE = PhyState()
