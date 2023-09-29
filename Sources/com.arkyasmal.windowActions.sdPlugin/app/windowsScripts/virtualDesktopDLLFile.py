import os
import curlify
import subprocess
import requests
import platform
from getMatchingWindowList import test_regex
import ctypes
import os  
def start_app_instance(file_version): 
    current_directory = os.path.dirname(os.path.abspath(__file__))
    vda = ctypes.WinDLL(f"{current_directory}/{file_version}")
    curr_desktop = vda.GetCurrentDesktopNumber()
    print(f'Virtual Desktop App Instance started on {curr_desktop}')
    return vda
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
def download_release_file():
    owner = "Ciantic"
    repo = "VirtualDesktopAccessor"
    file_path = "VirtualDesktopAccessor.dll"
    output_path = os.path.dirname(os.path.abspath(__file__))
    url = f"https://github.com/{owner}/{repo}/releases/latest"
    #file_url = f"https://github.com/{owner}/{repo}/releases/download/{tag}/{file_path}"
    #curl request
    session = requests.Session()
    response = session.get(url)
    curl_command = curlify.to_curl(response.request)
    #get latest tag
    # Define the pattern using regex
    pattern = r"VirtualDesktopAccessor/releases/tag/(.*)"
    # Use regex to find the matching string
    match = test_regex(pattern, curl_command)
    tag = ''
    if match:
        tag = match.group(1)
    else:
        print("No match found.")
        return 
    new_file_url = f"https://github.com/{owner}/{repo}/releases/download/{tag}/{file_path}"
    response = requests.get(new_file_url)
    if response.status_code == 200:
        data = None
        with open(f"{output_path}/dll/{file_path}", "wb") as f:
            f.write(response.content)
            data = response.content
        print("File downloaded successfully.")
        return data
    else:
        print("Failed to download file.")
        return None
#since this binary is changing, and we need to provide support
#for win 10 and up, we need to write logic that handles the correct use of the file
#as some binaries are not backwards compatiable
def determine_ddl_file_used():
    [major, revision] = get_build_num()
    if(major < 22000):
        return f'dll/VirtualDesktopAccessor-Win10.dll'
    elif(revision < 2215):
        return f'dll/VirtualDesktopAccessor-Win11v1.dll'
    else:
        win11v2 = f'dll/VirtualDesktopAccessor-Win11v2.dll'
        win11Latest = f'dll/VirtualDesktopAccessor.dll'
        try:
            start_app_instance(win11v2)
            return win11v2
        except OSError: 
            start_app_instance(win11Latest)
            return win11Latest
        except: 
            download_release_file()
            start_app_instance(win11Latest)
            return win11Latest