###
# DO NOT MOVE SCRIPT FROM ROOT OF PYTHON APP. IT WILL BREAK
# THE BUILD, AND RESULT IN IMPORT ERRORS!!
###
from cx_Freeze import setup, Executable
import os
import pathlib

plugin_name = 'com.arkyasmal.windowactions.sdPlugin'


def dll_path(file_name: str):
    current_working_dir = os.getcwd()
    new_path = os.path.normpath(os.path.abspath(
        os.path.join(current_working_dir, plugin_name, fr"app\dll\{file_name}")))
    new_path = pathlib.Path(new_path).as_posix()
    print(new_path)
    return (new_path, file_name)


def get_connection_path(str: str):
    current_working_dir = os.getcwd()
    new_path = os.path.normpath(os.path.abspath(
        os.path.join(current_working_dir, plugin_name, fr"app\scripts\{str}")))
    new_path = pathlib.Path(new_path).as_posix()
    return new_path


base = None
exe = Executable(get_connection_path("connection.py"), base=base)
include_files = [
    dll_path("VirtualDesktopAccessor-Win10.dll"),
    dll_path("VirtualDesktopAccessor-Win11v2.dll"),
    dll_path("VirtualDesktopAccessor-Win11v1.dll"),
    dll_path("VirtualDesktopAccessor-Win11v3.dll"),
    dll_path("VirtualDesktopAccessor-Win11latest.dll"),
]
include_packages = [
    "pywintypes",
    "win32gui",
    "win32process",
    "os",
    "ctypes",
    "pathlib",
    "win32con",
    "win32api",
    "win32gui",
    "functools",
    "win32com",
    "difflib",
    "websocket",
    "typing",
    "subprocess",
    "platform",
    "re",
    "pynput",
    "time",
    "json",
    "argparse",
    "rel",
    "wmi",
    "psutil"
]

options = {
    'packages': include_packages,
    "include_files": include_files,
    "build_exe": f"dist/{plugin_name}/bin",
}

setup(name="Window Actions",
      description="Window Actions",
      version="4.2.3",
      options={"build_exe": options},
      executables=[exe]
      )
