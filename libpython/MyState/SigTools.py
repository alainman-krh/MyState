#MyState/SigTools.py
#-------------------------------------------------------------------------------
from .Signals import SigAbstract, SigUpdate
from . import Signals

MAP_SIGCLS = {sig.TYPE: sig for sig in Signals.SIG_ALL}

#==StateObserverIF/SignalListenerIF
#===============================================================================
class StateObserverIF: #Interface class
	#@abstractmethod #Doesn't exist
	def handle_update(self, id_section:str):
		"""Returns: `wasproc` (was processed)"""
		pass

class SignalListenerIF: #Interface class
	#@abstractmethod #Doesn't exist
	def process_signal(self, sig:SigAbstract):
		"""Returns: `wasproc` (was processed)"""
		pass


#==Helper functions
#===============================================================================
def cliprng(rng, val):
	"""Clip val to within provided range"""
	return min(max(val, min(rng)), max(rng))

#-------------------------------------------------------------------------------
def _idsplit(idstr:str, valstr:str):
	#Get idstr components:
	idstr = idstr.strip()
	v_id = (idstr,) #If no suffix found
	sfx_start = idstr.find("(")
	if sfx_start >= 0: #Multipe suffixes detected: parse out
		sfx_end = idstr.find(")", sfx_start)
		if sfx_end < 0:
			return (tuple(), tuple()) #Should't be
		pfx = idstr[:sfx_start]
		sfx = idstr[sfx_start+1:sfx_end]
		v_sfx = sfx.split(",")
		v_id = tuple(pfx+sfx for sfx in v_sfx) #Re-combine
	N = len(v_id)

	#Get valstr components:
	valstr = valstr.strip()
	l_valstr = len(valstr)
	if (l_valstr > 2) and ("(" == valstr[0]) and (")" == valstr[-1]):
		valstr = valstr[1:-1] #Strip '()'
	v_val = valstr.split(",")
	Nval = len(v_val)
	if 1 == Nval and 0 == len(v_val[0]):
		v_val = tuple("0")*N
	elif Nval != N:
		return (tuple(), tuple()) #Should't be

	#Get numeric values... or fail
	try:
		v_val = tuple(int(v) for v in v_val)
	except:
		return (tuple(), tuple()) #Invalid values

	return (v_id, v_val)


#==API
#===============================================================================
def Signal_Deserialize(s:str):
	"""Supports command strings with multiple parameters.
	ex: `SET CFG:kitchen.(R,G,B) (240,180,0)`

	Returns a list of signals (typically just 1)"""
	idstr = ""; valstr = ""
	comp = s.split(" ") #String components
	N = len(comp)
	if N < 2 or N > 3:
		return tuple() #Not recognized

	#Signal
	sig = comp[0]
	sigcls = MAP_SIGCLS.get(sig, None)
	if sigcls is None:
		return tuple()

	#Value
	if N > 2:
		valstr = comp[2]

	#ID
	idcomp = comp[1].split(":")
	N = len(idcomp)
	if N < 1 or N > 2:
		return tuple() #Not recognized
	section = idcomp[0]
	if N > 1:
		idstr = idcomp[1]

	(v_id, v_val) = _idsplit(idstr, valstr)
	siglist = (sigcls(section, id, val) for (id, val) in zip(v_id, v_val))
	return siglist
