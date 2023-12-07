import os
import subprocess
import platform
from getMatchingWindowList import test_regex
import ctypes
import pathlib
ctypes.windll.kernel32.SetDllDirectoryW(None)
def start_app_instance(file_version): 
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file = fr"..\..\{file_version}"
    file_path = os.path.normpath(os.path.abspath(os.path.join(curr_dir, file)))
    command = pathlib.Path(file_path).as_posix()
    vda = ctypes.WinDLL(command)
    curr_desktop = vda.GetCurrentDesktopNumber()
    print(f'Virtual Desktop App Instance started on {curr_desktop}')
    return vda
def initialize_app_view(): 
    file_used = determine_ddl_file_used()
    app_instance = start_app_instance(file_used) 
    return app_instance
def get_build_num(): 
    win_ver = str(subprocess.check_output('ver', shell=True).rstrip())
    pattern = r'Version (.*)]'
    # Use regex to find the matching string
    match = test_regex(pattern, win_ver)
    full_ver_num = match.group(1)
    rev_pattern = r'\.([^.]*)$'
    rev_match = test_regex(rev_pattern, full_ver_num)
    revision_num = int(rev_match.group(1))
    kernel_version = platform.sys.getwindowsversion()
    build_num = kernel_version.build
    return [build_num, revision_num]
#since this binary is changing, and we need to provide support
#for win 10 and up, we need to write logic that handles the 
#correct use of the file as some binaries are not backwards compatiable
def determine_ddl_file_used():
    [major, revision] = get_build_num()
    if(major < 22000):
        return f'VirtualDesktopAccessor-Win10.dll'
    elif(revision < 2215):
        return f'VirtualDesktopAccessor-Win11v1.dll'
    else:
        win11v2 = f'VirtualDesktopAccessor-Win11v2.dll'
        win11Latest = f'VirtualDesktopAccessor.dll'
        try:
            start_app_instance(win11v2)
            return win11v2
        except OSError: 
            start_app_instance(win11Latest)
            return win11Latest
        except: 
            start_app_instance(win11Latest)
            return win11Latest