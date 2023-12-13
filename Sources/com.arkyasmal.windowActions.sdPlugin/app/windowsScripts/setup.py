from cx_Freeze import setup, Executable
import os
import pathlib
def dll_path(file_name:str ):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.normpath(os.path.abspath(os.path.join(current_dir,fr"..\dll\{file_name}" )))
    new_path = pathlib.Path(new_path).as_posix()
    return (new_path, file_name)
base = None
exe = Executable("connection.py", base=base)
include_files = [
      dll_path("VirtualDesktopAccessor-Win10.dll"),
      dll_path("VirtualDesktopAccessor-Win11v2.dll"),
      dll_path("VirtualDesktopAccessor-Win11v1.dll"),
      dll_path("VirtualDesktopAccessor.dll"),
]
include_packages = [
      "argparse",
      "json",
      "os",
      "sys",
      "json", 
      "websocket",
      "rel",
      "pywintypes",
      "win32gui",
      "win32con",
      "csv",
      "ctypes",
      "win32process",
      "win32api",
      "win32com",
      "functools",
      "difflib",
      "pathlib",
      "pynput",
      "wmi",
      "re",
      "pathlib"
]
options = {
    'packages': include_packages,
    # 'zip_exclude': zip_exclude,
    # "include_files": [

    # ],
    "include_files": include_files
}

setup(name="Window Actions",
      description="Window Actions",
      version="4.0.0",
      options={"build_exe": options},
      executables=[exe]
      )
