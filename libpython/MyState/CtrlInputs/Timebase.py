#Timebase.py
#-------------------------------------------------------------------------------
import sys

#Provides now_ms, ms_delta, ms_elapsed, ms_addwrap.
#NOTE: `now_ms` should be sufficient for most human-scale interactions.


try:
	import platform
	raise Exception("TODO")
except ImportError:
	if 'circuitpython' in sys.version.lower():
		from .CktPy.Timebase import *
	elif 'micropython' in sys.version.lower():
		raise Exception("TODO")
