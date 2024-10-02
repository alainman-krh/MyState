# upload.py: Upload code to CircuitPython board
#-------------------------------------------------------------------------------
from DevUtilsSupport import UploadProj
from os.path import join as joinpath

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
proj = "AFMacropad_LightCtrl"

proj = joinpath("demos", proj)
UploadProj(proj, DEST_DRIVE, refresh_libs=False)

#Last line