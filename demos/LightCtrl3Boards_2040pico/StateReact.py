#LightCtrl3Boards_2040pico\StateReact.py: React code to keep device states in sync
#-------------------------------------------------------------------------------
from StateDef import STATEBLK_CFG, STATEBLK_MAIN, MYSTATE, StateBlock
from MyState.Signals import SigToggle, SigIncrement, SigSet
from MyState.SigTools import StateObserverIF
from MyState.SigIO import SigCom

r"""COMMENTS:
- RoomRefCache / ._build_object_cache() below are NOT strictly necessary.
  Might be an over-optimization, especially given this is "user code" (not library code).
"""


#==Constants
#===============================================================================
SCALE_ENCTICK2LEVEL = 5 #Sensitivity: encoder tick to light level
SCALE_ENCTICK2COLOR = 15 #Sensitivity: encoder tick to color level


#==RoomRefCache: 
#===============================================================================
class RoomRefCache:
	"""Caches references to state data and identifier strings
	(simplifies math/code; create fewer temp strings/garbage collection)"""
	def __init__(self, id_light, idx):
		#NOTE: Ids cached for sending signals:
		#ALT: Allow ref to StateField_Int instead of just id string???
		self.id_enabled = id_light + ".enabled"
		self.id_level = id_light + ".level"
		self.id_R = id_light + ".R"
		self.id_G = id_light + ".G"
		self.id_B = id_light + ".B"
		self.id_light_by_idx = "light" + str(idx) #Reference light by hardware index (on dumb devices)

		#Field references for accessing state data:
		fields_cfg = STATEBLK_CFG.field_d
		self.R = fields_cfg[self.id_R]
		self.G = fields_cfg[self.id_G]
		self.B = fields_cfg[self.id_B]
		fields_main = STATEBLK_MAIN.field_d
		self.enabled = fields_main[self.id_enabled]
		self.level = fields_main[self.id_level]


#==MainStateSync: 
#===============================================================================
class MainStateSync(StateObserverIF):
	"""Reacts to changes in main state of LightControl system - keeping all
	attached devices/widgets synchronized.
	"""
	def __init__(self, light_idxmap:dict, update_comlist):
		"""-upadate_comlist: list<SigCom>. "Dumb devices" requiring updates to light color by index."""
		self.light_idxmap = light_idxmap
		self._build_object_cache()
		#Register to observe state changes (callback to .handle_update()):
		for blk in (STATEBLK_CFG, STATEBLK_MAIN):
			blk:StateBlock
			blk.observers_add(self)
		self.update_comlist = update_comlist

	def _build_object_cache(self):
		#Try to reduce object creation/garbage collection
		self.roomcache_map = {} #Pre-built strings/
		for (idx, id_light) in self.light_idxmap.items():
			self.roomcache_map[idx] = RoomRefCache(id_light, idx)
		#Sets light color/intensity as a single value understood by target device:
		self.sig_lightval_update = SigSet("Main", "light", 0)

	#Helper functions:
#-------------------------------------------------------------------------------
	def compute_color(self, refc:RoomRefCache):
		color_100 = (refc.R.val, refc.G.val, refc.B.val) #At full brightness
		scale = (refc.level.val / 100)
		scale *= refc.enabled.val
		return tuple(min(max(0, int(vi*scale)), 255) for vi in color_100)

	def update_lights(self):
		for (idx, refc) in self.roomcache_map.items():
			refc:RoomRefCache
			color = self.compute_color(refc)
			color_int24 = (color[0]<<16) | (color[1]<<8) | (color[2])
			self.sig_lightval_update.id = refc.id_light_by_idx
			self.sig_lightval_update.val = color_int24
			for com in self.update_comlist:
				#print("Signal KEYPAD", self.sig_lightval_update.serialize())
				com:SigCom
				com.send_signal(self.sig_lightval_update)

	#Refreshing macropad when state data changes
#-------------------------------------------------------------------------------
	def handle_update(self, id_section:str):
		"""Refreshes macropad after MYSTATE gets updated"""
		self.update_lights()

		if False: #Debug code: Print state
			section = None
			if "CFG" == id_section:
				section:StateBlock = STATEBLK_CFG
			elif "Main" == id_section:
				section:StateBlock = STATEBLK_MAIN
			else:
				return False
			for (id, field) in section.field_d.items():
				print(f"{id}: {field.val}")
			return True


#==SenseFilter: 
#===============================================================================
class SenseFilter:
	"""Manages/filters raw signals from sense devices, generating appropriate
	state-change signals (Indirection before affecting `MYSTATE`).

	Also maintains state of an "active light" being operated on (depends on last
	key pressed on macropad).
	"""
	def __init__(self, roomcache_map:dict):
		"""-roomcache_map: Constructed by `MainStateSync` object."""
		self.roomcache_map = roomcache_map
		self._build_object_cache()

	def _build_object_cache(self):
		#Try to reduce object creation/garbage collection (over-optimization??)
		self.sig_lighttoggle = SigToggle("Main", "") #id/room not specified
		self.sig_levelchange = SigIncrement("Main", "", 0)
		self.sig_colorchange_vect = tuple(SigIncrement("CFG", "", 0) for i in range(3))

	def lights_setactive(self, light_idx):
		refc:RoomRefCache = self.roomcache_map[light_idx]
		self.sig_lighttoggle.id = refc.id_enabled
		self.sig_levelchange.id = refc.id_level
		self.sig_colorchange_vect[0].id = refc.id_R
		self.sig_colorchange_vect[1].id = refc.id_G
		self.sig_colorchange_vect[2].id = refc.id_B

	def filter_keypress(self, light_idx):
		if light_idx not in self.roomcache_map.keys():
			return
		#Updates which light is affected by subsequent control signals (incl. sig_lighttoggle):
		self.lights_setactive(light_idx)
		MYSTATE.process_signal(self.sig_lighttoggle)

	def filter_MPencoder(self, delta):
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
