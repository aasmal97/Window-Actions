from cx_Freeze import setup, Executable
base = None
exe = Executable("connection.py", base=base) 
options = {
    'packages': [
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
      # "exchange",
      # "exchdapi",
    ],
    "include_files": [
      "dll/VirtualDesktopAccessor-Win10.dll",
      "dll/VirtualDesktopAccessor-Win11v2.dll",
      "dll/VirtualDesktopAccessor-Win11v1.dll",
      "dll/VirtualDesktopAccessor.dll",
    ],
}

setup(name="Window Actions",
      description="Window Actions",
      version="4.0.0",
      options={"build_exe": options},
      executables=[exe]
      )
