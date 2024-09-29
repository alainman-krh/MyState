#CktPy/Timebase.py
#-------------------------------------------------------------------------------
from supervisor import ticks_ms as now_ms
from micropython import const

#- `now_ms` should be sufficient for most human-scale interactions.
#- IR timing uses us timing (ex: pulseio backend).
#- Use `time.monotonic_ns()` for high-precision measurements instead.


#Timing values of supervisor module:
_SUPTICKS_WRAP = const(1<<29)
_SUPTICKS_MASK = const(_SUPTICKS_WRAP-1)
_SUPTICKS_HALFWRAP = const(_SUPTICKS_WRAP//2)

#-------------------------------------------------------------------------------
#Adapted from `ticks_diff` (https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html#supervisor.ticks_ms)
def ms_delta(t1, t0): #Notice subtracting 2nd arg.
	"""Compute the signed difference between two ticks_ms() values given # counter bits."""
	diff = (t1 - t0) & _SUPTICKS_MASK
	diff = ((diff + _SUPTICKS_HALFWRAP) & _SUPTICKS_MASK) - _SUPTICKS_HALFWRAP
	return diff

#-------------------------------------------------------------------------------
def ms_elapsed(t0, t1): #Notice t0 (ref) is first.
	"""Always positive"""
	return (t1 - t0) & _SUPTICKS_MASK

#-------------------------------------------------------------------------------
def ms_addwrap(t0, delta):
	"""Always positive"""
	return (t0 + delta) & _SUPTICKS_MASK
