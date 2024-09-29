#demos\NeoPixelControl_HomeAnalog\Main.py
#-------------------------------------------------------------------------------
from StateDef import STATEBLK_CFG, STATEBLK_MAIN, MYSTATE, StateBlock, PHYCTRL
from HAL_Macropad import KeypadElement, EncoderSense, KEYPAD_ENCODER
from MyState.Predefined.Buttons import EasyButton_Press
from MyState.Predefined.Buttons import EasyButton_SignalPressRel as KPButton
from MyState.Predefined.RotEncoders import EasyEncoder_Incr
from MyState.Signals import SigSet, SigGet, SigIncrement, SigToggle
from MyState.Signals import SigAbstract, SigUpdate
from MyState.Primitives import StateField_Int
from MyState.SigTools import SignalListenerIF


#==Main configuration
#===============================================================================
KPSWITCHES = {
	"kitchen": KeypadElement(0, "kitchen", PHYCTRL, "KP"),
	"room1": KeypadElement(1, "room1", PHYCTRL, "KP"),
}
#Context dependent. SigIncrement will be changed:
KPKNOB = EncoderSense(KEYPAD_ENCODER,
	#TODO: Find a way to scale by 1 when pressing down
	EasyEncoder_Incr(MYSTATE, SigIncrement("Main", "kitchen.level", 0)), scale = 5
)
#KPKNOB = EncoderSense(KEYPAD_ENCODER, EasyEncoder_Incr(MYSTATE, SigIncrement("Main", "NOCONN")))


#==RefreshAgent: Handles refreshing device when its state updates
#===============================================================================
class RefreshAgent(SignalListenerIF):
	"""Refreshes state after it gets updated (SigUpdate)"""
	def __init__(self, stateblock_list):
		for blk in stateblock_list:
			blk:StateBlock
			blk.listener_add(self)

	def compute_color(self, id_area, color_100):
		fields_main = STATEBLK_MAIN.field_d
		scale = (fields_main[id_area + ".level"].val / 100)
		scale *= fields_main[id_area + ".enabled"].val
		return tuple(int(vi*scale) for vi in color_100)

	def update_lights(self):
		color_100 = (255,255,255) #At full brightness

		for (id_area, sw) in KPSWITCHES.items():
			sw:KeypadElement
			color = self.compute_color(id_area, color_100)
			sw.pixel_set(color)

	def signal_process(self, sig:SigAbstract):
		if type(sig) != SigUpdate:
			return False

		sec = None
		if "CFG" == sig.section:
			sec:StateBlock = STATEBLK_CFG
		elif "Main" == sig.section:
			sec:StateBlock = STATEBLK_MAIN
			self.update_lights()
		else:
			return False

		#Just print out for now:
		for (id, field) in sec.field_d.items():
			print(f"{id}: {field.val}")
		return True


#==Global declarations
#===============================================================================
ragent = RefreshAgent([STATEBLK_CFG, STATEBLK_MAIN]) #Registers self listener


#==Main code entry
#===============================================================================
print("HELLO14")
STATEBLK_MAIN.signal_process(SigSet("Main", "kitchen.level", 5))
STATEBLK_MAIN.signal_process(SigSet("Main", "room1.level", 100))
while True:
	for sw in KPSWITCHES.values():
		sw.btn.process_inputs()
	KPKNOB.handler.process_withinputs(KPKNOB.pos_getdelta())
