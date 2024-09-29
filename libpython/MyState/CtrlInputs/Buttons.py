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


#=ButtonSensorIF
#===============================================================================
class ButtonSensorIF:
	#@abstractmethod
	def isactive(self):
		"""Is button active (typ: pressed)?"""
		pass


#=EasyButton
#===============================================================================
class EasyButton:
	"""EasyButton: Generic FSM implementation for interacting with buttons.
	USAGE: User derives this `EasyButton` & implements custom `handle_*` functions.

	NOTE:
	- `id`: In `hanle_*` events meant for convenience when 1 class definition
	        is used with multiple buttons.
	"""
	#Finite State Machine (FSM) controlling interations with buttons
	def __init__(self, id=None, btnsense:ButtonSensorIF=None, profile=Profiles.DEFAULT):
		self.id = id
		self.btnsense = btnsense
		self.profile = profile
		self._procfn_activestate = self._procfn_inactive
		self.press_start = now_ms()

#User-facing event handlers (optional/application-dependent)
#-------------------------------------------------------------------------------
	def handle_press(self, id):
		"""Button down"""
		pass
	def handle_longpress(self, id):
		pass
	def handle_doublepress(self, id):
		pass
	def handle_hold(self, id):
		"""Triggered every time `process_[with]inputs()` is called (when held)."""
		pass
	def handle_release(self, id):
		pass

#State-dependent (internal) event handlers
#-------------------------------------------------------------------------------
	def _procfn_inactive(self, isbtnactive): #Typ: Not pressed
		now = now_ms()
		sig_activate = isbtnactive #FSM signal
		if sig_activate:
			self.press_start = now
			self._procfn_activestate = self._procfn_heldshort
			self.handle_press(self.id)

	def _procfn_heldshort(self, isbtnactive): #Actively held (typ: pressed) for < LONGPRESS_MS
		profile = self.profile
		sig_release = (not isbtnactive) #FSM signal
		if sig_release:
			self._procfn_activestate = self._procfn_inactive
			self.handle_release(self.id)
			return
		
		now = now_ms()
		elapsed = ms_elapsed(self.press_start, now)
		sig_longpress = (elapsed >= profile.LONGPRESS_MS) #FSM signal
		if sig_longpress:
			self._procfn_activestate = self._procfn_heldlong
			self.handle_longpress(self.id)
			#Don't return. Still want to trigger hold event

		self.handle_hold(self.id)

	def _procfn_heldlong(self, isbtnactive): #Actively held (typ: pressed) for >= LONGPRESS_MS
		sig_release = (not isbtnactive) #FSM signal
		if sig_release:
			self._procfn_activestate = self._procfn_inactive
			self.handle_release(self.id)
			return

		self.handle_hold(self.id)

#Process inputs (and trigger events)
#-------------------------------------------------------------------------------
	def process_withinputs(self, isbtnactive):
		"""Provide inputs explicitly"""
		self._procfn_activestate(isbtnactive)

	def process_inputs(self):
		isbtnactive = self.btnsense.isactive() #`.btnsense` must be specified to call.
		self._procfn_activestate(isbtnactive)

#Last line
