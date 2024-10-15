# UploadTools.py: Support tools for uploading code to microcontroller
#-------------------------------------------------------------------------------
from os.path import join as joinpath
from os.path import basename, dirname, abspath
import shutil
import glob

_THIS_FILE = abspath(__file__); _THIS_DIR = dirname(_THIS_FILE)
_THIS_REPO = abspath(joinpath(_THIS_DIR, "..", "..", ".."))

SYNC_LIBS = [
	joinpath("libpython", "MyState"),
	joinpath("lib_cktpy", "EasyCktIO"),
]

#-------------------------------------------------------------------------------
def UploadProj(proj, dest_drive, refresh_libs=True):
	"proj: path relative to `MyState` root folder"

	#TODO: Check to make sure all libs are installed???
	#dest = _THIS_REPO #DEBUG
	print(f"Writing to {dest_drive}...")
	if refresh_libs:
		for relpath_lib in SYNC_LIBS:
			lib = basename(relpath_lib)
			print(f"Synchronizing lib '{lib}'...")
			src = joinpath(_THIS_REPO, relpath_lib)
			dest = joinpath(dest_drive, "lib", lib)
			#print(src, dest) #DEBUG
			shutil.copytree(src, dest, dirs_exist_ok=True)

	print(f"Synchronizing '{proj}'...")

	for src in glob.glob(joinpath(_THIS_REPO, proj, "*.py")):
		if ("main.py" in src) or ("code.py" in src):
			continue #Don't: Will restart chip
		dest = joinpath(dest_drive, basename(src))
		#print(src, dest) #DEBUG
		shutil.copyfile(src, dest)
	src = joinpath(_THIS_REPO, proj, "main.py") #Will restart chip
	dest = joinpath(dest_drive, basename(src))
	shutil.copyfile(src, dest)


	print("DONE.")
	print("\nREMINDER: Use a terminal program to access serial monitor (like putty).")
#Last line