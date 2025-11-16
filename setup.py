import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["pygame", "os", "sys", "random", "math"],
    "include_files": ["assets/"]  # Include the entire assets folder
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this to hide the console window

setup(
    name="HandMan",
    version="1.0",
    description="HandMan - Collect the Fingers!",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="HandMan.exe")]
)
