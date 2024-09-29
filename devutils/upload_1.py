# upload.py: Upload code to CircuitPython board
#-------------------------------------------------------------------------------
from DevUtilsSupport import UploadProj
from os.path import join as joinpath

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
proj = "NeoPixelControl_HomeAnalog"

proj = joinpath("demos", proj)
UploadProj(proj, DEST_DRIVE, refresh_libs=True)

#Last line