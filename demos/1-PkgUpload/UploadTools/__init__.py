# UploadTools.py: Support tools for uploading code to microcontroller
#-------------------------------------------------------------------------------
from os.path import join as joinpath
from os.path import basename, dirname, abspath, expandvars
import os
import tomllib
import shutil

_THIS_FILE = abspath(__file__); _THIS_DIR = dirname(_THIS_FILE)
_PROJROOT = abspath(joinpath(_THIS_DIR, "..", "..", ".."))


#=Helper functions
#===============================================================================
def path_eval(expr):
	"Substitutes environment variables & sanitizes results with abspath()"
	return abspath(expandvars(expr))

def UpdateEnv(pkg, dest_drive):
	os.environ["PROJROOT"] = _PROJROOT
	os.environ["THISPKG"] = joinpath(_PROJROOT, "pkg_install", pkg)
	os.environ["BOARDROOT"] = abspath(dest_drive)

def UploadFromFileDict(copyinfo:dict):
	"""Uploads from a dictionary of files/folders"""
	path_dest_root = path_eval(copyinfo["dest"])
	folder_list = copyinfo.get("folders", tuple())
	file_list = copyinfo.get("files", tuple())

	for fld_src in folder_list:
		path_src = path_eval(fld_src)
		id = basename(path_src)
		print(f"Uploading folder '{id}'...")
		path_dest = joinpath(path_dest_root, id)
		#print(path_src, path_dest) #DEBUG
		shutil.copytree(path_src, path_dest, dirs_exist_ok=True)

	for file_src in file_list:
		path_src = path_eval(file_src)
		id = basename(path_src)
		print(f"Uploading file '{id}'...")
		path_dest = joinpath(path_dest_root, id)
		#print(path_src, path_dest) #DEBUG
		shutil.copyfile(path_src, path_dest)


#=UploadPkg
#===============================================================================
def UploadPkg(pkg, dest_drive, refresh_libs=True):
	"proj: path relative to `MyState` root folder"	
	UpdateEnv(pkg, dest_drive) #Prepare environment variables

	#Read in `pydrv_install.toml` definition:	
	cfg = None #Define scope
	install_toml = path_eval("$THISPKG/pydrv_install.toml")
	with open(install_toml, "rb") as f:
		cfg = tomllib.load(f)

	if not refresh_libs:
		print("""\n==== Skipping module libraries ====""")
	else:
		#Upload files from Circuit Python bundle library
		print("""\n==== Uploading from "bundle" library ====""")
		modules_cpybundle = cfg["modules"].get("CPYBUNDLE", None)
		libpath_cpybundle = os.environ.get("LIBPATH_CPYBUNDLE", None)
		if modules_cpybundle is None:
			print("""No "bundle" library files to copy.""")
		elif libpath_cpybundle is None:
			print("NOTE: env:$LIBPATH_CPYBUNDLE not defined.")
			print("""==> Will not upload modules from Circuit Python "bundle" library.""")
		else:
			UploadFromFileDict(modules_cpybundle)

		print("""\n==== Uploading custom modules ====""")
		UploadFromFileDict(cfg["modules"])

	print("""\n==== Uploading package-specific files ====""")
	UploadFromFileDict(cfg["package"])

	print("\nPackage upload complete.")
	print("REMINDER: Use a terminal program to access serial monitor (like putty).")
#Last line