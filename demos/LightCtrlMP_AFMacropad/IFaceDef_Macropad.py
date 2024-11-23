#demos\LightCtrlMP_AFMacropad\IFaceDef_Macropad.py
#-------------------------------------------------------------------------------
from StateDef import STATEBLK_CFG, STATEBLK_MAIN, MYSTATE, StateBlock
from MyState.Signals import SigAbstract, SigUpdate, SigToggle, SigIncrement
from MyState.SigTools import StateObserverIF
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER


#==Constants
#===============================================================================
SCALE_ENCTICK2LEVEL = 5 #Sensitivity: encoder tick to light level
SCALE_ENCTICK2COLOR = 15 #Sensitivity: encoder tick to color level


#==RoomConfig: 
#===============================================================================
class RoomConfig:
	"""Caches references to state data
	(simplifies math/code; create fewer temp strings/garbage collection)"""
	def __init__(self, id_light):
		#NOTE: Ids cached for sending signals:
		#ALT: Allow ref to StateField_Int instead of just id string???
		self.id_enabled = id_light + ".enabled"
		self.id_level = id_light + ".level"
		self.id_R = id_light + ".R"
		self.id_G = id_light + ".G"
		self.id_B = id_light + ".B"

		#Field references for accessing state data:
		fields_cfg = STATEBLK_CFG.field_d
		self.R = fields_cfg[self.id_R]
		self.G = fields_cfg[self.id_G]
		self.B = fields_cfg[self.id_B]
		fields_main = STATEBLK_MAIN.field_d
		self.enabled = fields_main[self.id_enabled]
		self.level = fields_main[self.id_level]


#==PhyController: 
#===============================================================================
class PhyController(StateObserverIF):
	"""Manages state of physical control panel (vs core device function: MYSTATE).
	Also: Handles refreshing device on `.handle_update()`.
	"""
	def __init__(self, map_switches):
		self.keymap = {}
		for (btnidx, id_light) in map_switches.items():
			self.keymap[id_light] = KeypadElement(idx=btnidx)
		self.encknob = KEYPAD_ENCODER
		self.area_active = "NoneYet"
		self._build_object_cache()
		#Register to observe state changes (callback to .handle_update()):
		for blk in (STATEBLK_CFG, STATEBLK_MAIN):
			blk:StateBlock
			blk.observers_add(self)

	def _build_object_cache(self):
		#Try to reduce object creation/garbage collection
		self.roomstate_map = {}
		for id_light in self.keymap.keys():
			self.roomstate_map[id_light] = RoomConfig(id_light)
		self.sig_lighttoggle = SigToggle("Main", "") #id/room not specified
		self.sig_levelchange = SigIncrement("Main", "", 0)
		self.sig_colorchange_vect = tuple(SigIncrement("CFG", "", 0) for i in range(3))

	#Synchronizing macropad with MYSTATE
#-------------------------------------------------------------------------------
	def compute_color(self, cfg:RoomConfig):
		color_100 = (cfg.R.val, cfg.G.val, cfg.B.val) #At full brightness
		scale = (cfg.level.val / 100)
		scale *= cfg.enabled.val
		return tuple(int(vi*scale) for vi in color_100)

	def update_lights(self):
		for (id_light, sw) in self.keymap.items():
			sw:KeypadElement
			cfg = self.roomstate_map[id_light]
			color = self.compute_color(cfg)
			sw.pixel_set(color)

	#Refreshing macropad when state data changes
#-------------------------------------------------------------------------------
	def handle_update(self, section:str):
		"""Refreshes macropad after MYSTATE gets updated"""
		section = None
		if "CFG" == section:
			section:StateBlock = STATEBLK_CFG
		elif "Main" == section:
			section:StateBlock = STATEBLK_MAIN
		else:
			return False
		self.update_lights()

		if False: #Debug code: Print state
			for (id, field) in section.field_d.items():
				print(f"{id}: {field.val}")
			return True

	#Processing macropad sense inputs (Indirection before affecting `MYSTATE`)
#-------------------------------------------------------------------------------
	def lights_setactive(self, id_newarea):
		self.area_active = id_newarea
		cfg:RoomConfig = self.roomstate_map[id_newarea]
		self.sig_lighttoggle.id = cfg.id_enabled
		self.sig_levelchange.id = cfg.id_level
		self.sig_colorchange_vect[0].id = cfg.id_R
		self.sig_colorchange_vect[1].id = cfg.id_G
		self.sig_colorchange_vect[2].id = cfg.id_B

	def filter_keypress(self, id_light):
		self.lights_setactive(id_light) #Updates sig_lighttoggle.id
		MYSTATE.process_signal(self.sig_lighttoggle)

	def filter_KPencoder(self, delta):
		self.sig_levelchange.val = delta*SCALE_ENCTICK2LEVEL
		MYSTATE.process_signal(self.sig_levelchange)

	def filter_I2Cencoder(self, idx, delta):
		if idx not in range(4):
			return #Can't don anything.
		if 3 == idx:
			self.sig_levelchange.val = delta*SCALE_ENCTICK2LEVEL
			MYSTATE.process_signal(self.sig_levelchange)
		else:
			sig = self.sig_colorchange_vect[idx]
			sig.val = delta*SCALE_ENCTICK2COLOR
			MYSTATE.process_signal(sig)
