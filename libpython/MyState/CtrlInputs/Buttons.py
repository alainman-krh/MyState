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
		self.pevents_currentstate = self._pevents_up
		self.press_start = now_ms()

#State-dependent (internal) event handlers
#-------------------------------------------------------------------------------
	def _pevents_up(self, pressed):
		now = now_ms()
		if pressed:
			self.press_start = now
			self.pevents_currentstate = self._pevents_press
			self.handle_press(self.id)

	def _pevents_press(self, pressed): #Singlepress
		now = now_ms()
		profile = self.profile
		if pressed:
			elapsed = ms_elapsed(self.press_start, now)
			if elapsed >= profile.LONGPRESS_MS:
				self.pevents_currentstate = self._pevents_longpress
				self.handle_longpress(self.id)
			self.handle_hold(self.id)
		else:
			self.pevents_currentstate = self._pevents_up
			self.handle_release(self.id)

	def _pevents_longpress(self, pressed):
		if pressed:
			self.handle_hold(self.id)
		else:
			self.pevents_currentstate = self._pevents_up
			self.handle_release(self.id)

#Process button events
#-------------------------------------------------------------------------------
	def process_events(self, state_pressed):
		self.pevents_currentstate(state_pressed)

#Last line
