#demos\AFMacropad_LightCtrl\IFaceDef_Macropad.py
#-------------------------------------------------------------------------------
from StateDef import STATEBLK_CFG, STATEBLK_MAIN, MYSTATE, StateBlock
from MyState.Signals import SigAbstract, SigUpdate, SigToggle, SigIncrement
from MyState.SigTools import SignalListenerIF
from MyState.Predefined.RotEncoders import EasyEncoder_Signal
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER


#==PhyController: 
#===============================================================================
class PhyController(SignalListenerIF):
	"""Manages state of physical control panel (vs core device function: MYSTATE).
	Also: Handles refreshing device on state `.update()`.
	"""
	def __init__(self, map_switches):
		self.keymap = {}
		for (btnidx, area) in map_switches.items():
			self.keymap[area] = KeypadElement(self, "KP", area, idx=btnidx)
		self.encknob = EasyEncoder_Signal(self, "KP", "KPenc", KEYPAD_ENCODER)
		self.area_active = "NoneYet"
		self._build_object_cache()
		#Register to observe state changes (callback to .update()):
		for blk in (STATEBLK_CFG, STATEBLK_MAIN):
			blk:StateBlock
			blk.observers_add(self)

	def _build_object_cache(self):
		#Try to reduce object creation/garbage collection
		self.strmap_roomenabled = {}
		self.strmap_roomlevel = {}
		self.strmap_roomcolor = {}
		for area in self.keymap.keys():
			self.strmap_roomenabled[area] = area+".enabled"
			self.strmap_roomlevel[area] = area+".level"
			self.strmap_roomcolor[area] = (area+".R", area+".G", area+".B")
		self.sig_lighttoggle = SigToggle("Main", "") #id/room not specified
		self.sig_kpenc = SigIncrement("Main", "", 0)

	#Synchronizing macropad with MYSTATE
#-------------------------------------------------------------------------------
	def compute_color(self, id_area, color_100):
		fields_main = STATEBLK_MAIN.field_d
		id_level = self.strmap_roomlevel[id_area]
		id_enabled = self.strmap_roomenabled[id_area]
		scale = (fields_main[id_level].val / 100)
		scale *= fields_main[id_enabled].val
		return tuple(int(vi*scale) for vi in color_100)

	def update_lights(self):
		fields_cfg = STATEBLK_CFG.field_d
		color_100 = [255, 255, 255] #At full brightness
		for (id_area, sw) in self.keymap.items():
			idRGB = self.strmap_roomcolor[id_area]
			for (i, id) in enumerate(idRGB): #Get individual RGB values
				color_100[i] = fields_cfg[id].val
			sw:KeypadElement
			color = self.compute_color(id_area, color_100)
			sw.pixel_set(color)

	#Refreshing macropad when state data changes
#-------------------------------------------------------------------------------
	def update(self, sig:SigUpdate):
		"""Refreshes macropad after MYSTATE gets updated"""
		sec = None
		if "CFG" == sig.section:
			sec:StateBlock = STATEBLK_CFG
		elif "Main" == sig.section:
			sec:StateBlock = STATEBLK_MAIN
			self.update_lights()
		else:
			return False

		if False: #Debug code: Print state
			for (id, field) in sec.field_d.items():
				print(f"{id}: {field.val}")
			return True

	#Processing macropad sense inputs (Main state control bypasses this)
#-------------------------------------------------------------------------------
	def area_setactive(self, newarea):
		self.area_active = newarea
		self.sig_lighttoggle.id = self.strmap_roomenabled[newarea]
		self.sig_kpenc.id = self.strmap_roomlevel[newarea]

	def process_signal(self, sig:SigAbstract):
		if "kitchen.press" == sig.id:
			self.area_setactive("kitchen") #Updates sig_lighttoggle.id
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "room1.press" == sig.id:
			self.area_setactive("room1")
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "KPenc.change" == sig.id:
			self.sig_kpenc.val = sig.val
			MYSTATE.process_signal(self.sig_kpenc)

	def process_inputs(self): #Triggers `.process_signal()`
		for sw in self.keymap.values():
			sw:KeypadElement
			sw.btn.process_inputs()
		self.encknob.process_inputs()
