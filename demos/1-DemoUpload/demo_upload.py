#demo_upload.py: Upload demo code to CircuitPython board
#-------------------------------------------------------------------------------
from UploadTools import UploadProj
from os.path import join as joinpath

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
proj = "LightCtrlMP_AFMacropad"
#proj = "TestSerial_AFMacropad"
#proj = "TestSerial_RP2040"

proj = joinpath("demos", proj)
UploadProj(proj, DEST_DRIVE, refresh_libs=True)

#Last line