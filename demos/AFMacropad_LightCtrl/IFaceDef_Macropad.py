#demos\AFMacropad_LightCtrl\IFaceDef_Macropad.py
#-------------------------------------------------------------------------------
from StateDef import STATEBLK_CFG, STATEBLK_MAIN, MYSTATE, StateBlock
from MyState.Signals import SigAbstract, SigUpdate, SigToggle, SigIncrement
from MyState.SigTools import SignalListenerIF
from MyState.Predefined.RotEncoders import EasyEncoder_Signal
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER


#==RoomConfig: 
#===============================================================================
class RoomConfig:
	"""Caches references to state data
	(simplifies code; create fewer temp strings/garbage collection)"""
	def __init__(self, id_area):
		#NOTE: Ids cached for sending signals:
		#ALT: Allow ref to StateField_Int instead of just id string???
		self.id_enabled = id_area + ".enabled"
		self.id_level = id_area + ".level"

		fields_main = STATEBLK_CFG.field_d
		self.R = fields_main[id_area + ".R"]
		self.G = fields_main[id_area + ".G"]
		self.B = fields_main[id_area + ".B"]
		fields_main = STATEBLK_MAIN.field_d
		self.enabled = fields_main[self.id_enabled]
		self.level = fields_main[self.id_level]


#==PhyController: 
#===============================================================================
class PhyController(SignalListenerIF):
	"""Manages state of physical control panel (vs core device function: MYSTATE).
	Also: Handles refreshing device on state `.update()`.
	"""
	def __init__(self, map_switches):
		self.keymap = {}
		for (btnidx, id_area) in map_switches.items():
			self.keymap[id_area] = KeypadElement(self, "KP", id_area, idx=btnidx)
		self.encknob = EasyEncoder_Signal(self, "KP", "KPenc", KEYPAD_ENCODER)
		self.area_active = "NoneYet"
		self._build_object_cache()
		#Register to observe state changes (callback to .update()):
		for blk in (STATEBLK_CFG, STATEBLK_MAIN):
			blk:StateBlock
			blk.observers_add(self)

	def _build_object_cache(self):
		#Try to reduce object creation/garbage collection
		self.roomstate_map = {}
		for id_area in self.keymap.keys():
			self.roomstate_map[id_area] = RoomConfig(id_area)
		self.sig_lighttoggle = SigToggle("Main", "") #id/room not specified
		self.sig_kpenc = SigIncrement("Main", "", 0)

	#Synchronizing macropad with MYSTATE
#-------------------------------------------------------------------------------
	def compute_color(self, cfg:RoomConfig):
		color_100 = (cfg.R.val, cfg.G.val, cfg.B.val) #At full brightness
		scale = (cfg.level.val / 100)
		scale *= cfg.enabled.val
		return tuple(int(vi*scale) for vi in color_100)

	def update_lights(self):
		for (id_area, sw) in self.keymap.items():
			sw:KeypadElement
			cfg = self.roomstate_map[id_area]
			color = self.compute_color(cfg)
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
	def area_setactive(self, id_newarea):
		self.area_active = id_newarea
		cfg:RoomConfig = self.roomstate_map[id_newarea]
		self.sig_lighttoggle.id = cfg.id_enabled
		self.sig_kpenc.id = cfg.id_level

	def process_signal(self, sig:SigAbstract):
		if "kitchen.press" == sig.id:
			self.area_setactive("kitchen") #Updates sig_lighttoggle.id
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "livingroom.press" == sig.id:
			self.area_setactive("livingroom")
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "garage.press" == sig.id:
			self.area_setactive("garage")
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "bedroom1.press" == sig.id:
			self.area_setactive("bedroom1")
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "bedroom2.press" == sig.id:
			self.area_setactive("bedroom2")
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "bedroom3.press" == sig.id:
			self.area_setactive("bedroom3")
			MYSTATE.process_signal(self.sig_lighttoggle)
		elif "KPenc.change" == sig.id:
			self.sig_kpenc.val = sig.val
			MYSTATE.process_signal(self.sig_kpenc)

	def process_inputs(self): #Triggers `.process_signal()`
		for sw in self.keymap.values():
			sw:KeypadElement
			sw.btn.process_inputs()
		self.encknob.process_inputs()
