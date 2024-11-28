#demo_upload.py: Upload demo code to CircuitPython board
#-------------------------------------------------------------------------------
from UploadTools import UploadProj
from os.path import join as joinpath

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
proj = "LightCtrl3Boards_2040pico"
#proj = "LightCtrl3Boards_AFMacropad"
#proj = "LightCtrl3Boards_CPbluefruit"
#proj = "LightCtrlMP_AFMacropad"

proj = joinpath("demos", proj)
UploadProj(proj, DEST_DRIVE, refresh_libs=True)

#Last line