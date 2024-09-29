#MyState/CtrlInputs.py
#-------------------------------------------------------------------------------
from .Timebase import now_ms, ms_elapsed

#TODO: Debounce


#=Behavioural profiles
#===============================================================================
class Profile:
	def __init__(self, DEBOUNCE_MS=100, LONGPRESS_MS=2000, DBLPRESSMAX_MS=1000):
		#How long something must be held to count as pressed:
		self.DEBOUNCE_MS = DEBOUNCE_MS
		#How long something needs to be held to be considered a "long press":
		self.LONGPRESS_MS = LONGPRESS_MS
		#Maximum time between press events for something to be considered a "double-press":
		self.DBLPRESSMAX_MS = DBLPRESSMAX_MS
		pass

class Profiles:
	DEFAULT = Profile()
	#TODO: Add more profiles!


#=EasyButtonIF
#===============================================================================
class EasyButtonIF:
	"""NOTE
	- `id`: In `hanle_*` events meant for convenience when 1 class definition
	        is used with multiple buttons.
	"""
	#@abstractmethod
	def process_events(self, state_pressed):
		"""Also updates state-tracking data (Typically: Only run once per loop)"""
		pass

#User-facing event handlers (optionally/application-dependent)
#-------------------------------------------------------------------------------
	def handle_press(self, id):
		"""Button down"""
		pass
	def handle_longpress(self, id):
		pass
	def handle_doublepress(self, id):
		pass
	def handle_hold(self, id):
		"""Triggered every time process_events() is called"""
		pass
	def handle_release(self, id):
		pass


#=EasyButton
#===============================================================================
class EasyButton(EasyButtonIF):
	"""EasyButton: Generic FSM implementation for interacting with buttons
	(Must implement event handlers declared in interface `EasyButtonIF`.)
	"""
	#Finite State Machine (FSM) controlling interations with buttons
	def __init__(self, id=None, profile=Profiles.DEFAULT):
		self.id = id
		self.profile = profile
		self._statefn_active = self._statefn_inactive
		self.press_start = now_ms()

#State-dependent (internal) event handlers
#-------------------------------------------------------------------------------
	def _statefn_inactive(self, pressed): #Typ: Not pressed
		now = now_ms()
		det_activate = pressed #FSM signal
		if det_activate:
			self.press_start = now
			self._statefn_active = self._statefn_heldshort
			self.handle_press(self.id)

	def _statefn_heldshort(self, pressed): #Actively held (typ: pressed) for < LONGPRESS_MS
		profile = self.profile
		det_release = (not pressed) #FSM signal
		if det_release:
			self._statefn_active = self._statefn_inactive
			self.handle_release(self.id)
			return
		
		now = now_ms()
		elapsed = ms_elapsed(self.press_start, now)
		det_longpress = (elapsed >= profile.LONGPRESS_MS) #FSM signal
		if det_longpress:
			self._statefn_active = self._statefn_heldlong
			self.handle_longpress(self.id)
			#Don't return. Still want to trigger hold event

		self.handle_hold(self.id)

	def _statefn_heldlong(self, pressed): #Actively held (typ: pressed) for >= LONGPRESS_MS
		det_release = (not pressed) #FSM signal
		if det_release:
			self._statefn_active = self._statefn_inactive
			self.handle_release(self.id)
			return

		self.handle_hold(self.id)

#Process button events
#-------------------------------------------------------------------------------
	def process_events(self, state_pressed):
		self._statefn_active(state_pressed)

#Last line
