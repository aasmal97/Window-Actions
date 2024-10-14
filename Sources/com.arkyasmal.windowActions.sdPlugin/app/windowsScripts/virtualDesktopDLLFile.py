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
    return [int(build_num), int(revision_num)]
# since this binary is changing, and we need to provide support
# for win 10 and up, we need to write logic that handles the
# correct use of the file as some binaries are not backwards compatiable


def attempt_ddl_ver(ver1: str, ver2: str):
    try:
        start_app_instance(ver1)
        return ver1
    except OSError:
        start_app_instance(ver2)
        return ver2
    except:
        start_app_instance(ver2)
        return ver2


def determine_ddl_file_used():
    [major, revision] = get_build_num()
    if (major < 22000):
        # works with old dll version
        if (major < 19045 or (major == 19045 and revision < 4123)):
            return f'VirtualDesktopAccessor-Win10.dll'
        # requires newest dll version similar to windows 11
        elif (major >= 19045):
            return f'VirtualDesktopAccessor-Win11latest.dll'
    elif (major < 22635):
        if (major < 22621 or (major == 22621 and revision < 2215)):
            return f'VirtualDesktopAccessor-Win11v1.dll'
        elif (major == 22621 and revision < 3155):
            return attempt_ddl_ver(f'VirtualDesktopAccessor-Win11v2.dll', f'VirtualDesktopAccessor-Win11v3.dll')
        else:
            return attempt_ddl_ver(f'VirtualDesktopAccessor-Win11latest.dll', f'VirtualDesktopAccessor-Win11latest.dll')
    # retain version of previous files
    elif (major == 22635 and revision < 2915):
        return attempt_ddl_ver(f'VirtualDesktopAccessor-Win11v2.dll', f'VirtualDesktopAccessor-Win11v3.dll')
    # due to changes after 22635.2915, this needs an update
    else:
        return attempt_ddl_ver(f'VirtualDesktopAccessor-Win11latest.dll', f'VirtualDesktopAccessor-Win11latest.dll')
