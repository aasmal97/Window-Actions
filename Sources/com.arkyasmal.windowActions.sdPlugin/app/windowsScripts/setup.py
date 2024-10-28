from cx_Freeze import setup, Executable
import os
import pathlib


def dll_path(file_name: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.normpath(os.path.abspath(
        os.path.join(current_dir, fr"..\dll\{file_name}")))
    new_path = pathlib.Path(new_path).as_posix()
    return (new_path, file_name)


base = None
exe = Executable("connection.py", base=base)
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
    "csv",
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
    "wmi"
]
# include_packages = [
#     "argparse",
#     "json",
#     "os",
#     "sys",
#     "json",
#     "websocket",
#     "rel",
#     "pywintypes",
#     "win32gui",
#     "win32con",
#     "csv",
#     "ctypes",
#     "win32process",
#     "win32api",
#     "win32com",
#     "functools",
#     "difflib",
#     "pynput",
#     "wmi",
#     "re",
#     "pathlib"
# ]
options = {
    'packages': include_packages,
    "include_files": include_files,
    'build_exe': "dist"
}

setup(name="Window Actions",
      description="Window Actions",
      version="4.2.1",
      options={"build_exe": options},
      executables=[exe]
      )
