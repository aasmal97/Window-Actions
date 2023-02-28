from pyvda import AppView, VirtualDesktop, get_virtual_desktops
from determineActiveWindows import get_active_windows
import sys
import re
import pywintypes
from win32api import EnumDisplayMonitors, GetMonitorInfo, EnumDisplayDevices
from win32gui import MoveWindow, GetWindowRect
from win32com.client import GetObject
from pynput.keyboard import Key, Controller
import functools
from difflib import SequenceMatcher
import os
import json
from pathlib import Path
def create_json_file(data, app_data_directory):
    new_data_json = json.dumps(data)
    directory_path = Path(f'{os.getenv("APPDATA")}\\{app_data_directory}')
    if not directory_path.exists():
        os.makedirs(directory_path)
    path_to_file = directory_path / 'currentMonitors.json'
    path_to_file = path_to_file.resolve()
    try:
        f = open(path_to_file, "x")
        f.write(new_data_json)
        return new_data_json
    except FileExistsError:
        f = open(path_to_file, "w")
        f.write(new_data_json)
        return new_data_json
    except: 
        print("An error occured")
def test_regex(pattern, testStr):
    result = re.search(pattern, testStr)
    return result
def create_new_desktop(): 
    keyboard = Controller()
    keyboard.press(Key.cmd)
    keyboard.press(Key.ctrl)
    keyboard.press("d")
    keyboard.release("d")
    keyboard.release(Key.ctrl)
    keyboard.release(Key.cmd)
def create_new_virtual_desktop(desktopsToCreate: int):
    curr_desktop = VirtualDesktop.current().number
    for x in range(desktopsToCreate):
        create_new_desktop()
    move_virtual_desktop(curr_desktop)
def check_desktops(num: int):
    desktop_available = len(get_virtual_desktops())
    if num > desktop_available:
        create_new_virtual_desktop(num - desktop_available)
def move_virtual_desktop(num: int):
    check_desktops(num)
    target_desktop = VirtualDesktop(num)
    target_desktop.go()
    return "Moved to this virtual desktop"
def move_window(hwnd, num): 
    check_desktops(num)
    window: AppView
    if isinstance(hwnd, int) or isinstance(str): 
        window = AppView(hwnd)
    else: 
        window = AppView.current()
    target_desktop = VirtualDesktop(num)
    window.move(target_desktop)
    return f'successfully moved to desktop {num}'
def convert_unit16_to_str(arr):
    chr_list = [chr(x) for x in arr]
    filtered_list = list(filter( lambda char: len(char)<=1, chr_list))
    new_str = functools.reduce(lambda a,b: a+b, filtered_list)
    return new_str.rstrip('\x00')
def get_monitor_names(app_data_directory):
    names = [GetMonitorInfo(x[0])["Device"] for x in EnumDisplayMonitors()] 
    monitor_ids = [EnumDisplayDevices( names[x],0, 1).DeviceID.replace("#", "\\") for x in range(len(names))]
    obj_wmi = GetObject('winmgmts:\\\\.\\root\\WMI').InstancesOf('WmiMonitorID')  # WmiMonitorConnectionParams
    instance_names = [dict(instance_name = item.InstanceName, name = convert_unit16_to_str(item.UserFriendlyName)) for item in obj_wmi]
    for instance in instance_names:
        highest_match = {"match":"", "idx": 0}
        for idx in range(len(monitor_ids)):
            pattern = instance['instance_name'].replace("\\", " ")
            test_str = monitor_ids[idx].replace("\\", " ")
            sequence = SequenceMatcher(None, pattern, test_str).find_longest_match(0, len(pattern), 0, len(test_str))
            matching_str = test_str[sequence.a:sequence.a + sequence.size]
            if len(matching_str) > len(highest_match['match']):
                highest_match.update({'match': matching_str, "idx": idx})
            print(pattern, test_str, matching_str)
        # we want the idx to be 1-indexed
        instance.update({"idx": highest_match["idx"] + 1})
    create_json_file(instance_names, app_data_directory)
    return instance_names
def move_window_to_monitor(hwnd: str, num: int):
    monitors = [GetMonitorInfo(x[0])['Monitor'] for x in EnumDisplayMonitors()]
    monitor_selected = monitors[num]
    window_to_move = GetWindowRect(hwnd)
    monitor_width = abs(monitor_selected[0] - monitor_selected[2])
    monitor_height = abs(monitor_selected[1] - monitor_selected[3])
    window_width = abs(window_to_move[0] - window_to_move[2])
    window_height = abs(window_to_move[1] - window_to_move[3])
    new_window_width = monitor_width if window_width > monitor_width else window_width
    new_window_height = monitor_height if window_height > monitor_height else window_height
    MoveWindow(hwnd, monitor_selected[0], monitor_selected[1], new_window_width, new_window_height, True)
    return f'successfully moved to monitor {num}'

def get_matching_windows_list(win_id_type, win_id):
    id_type = "title" if win_id_type == 'win_title' or win_id_type == 'win_ititle' else win_id_type
    is_partial_str = win_id_type == 'win_ititle'
    file_path = "Elgato\StreamDeck\Plugins\com.arkyasmal.windowActions.txt"
    all_windows = get_active_windows(app_data_directory = file_path)
    matching_windows_itr = filter(lambda window: test_regex(win_id, window[id_type]) if is_partial_str else window[id_type] == win_id, all_windows)
    matching_windows = list(matching_windows_itr)
    return matching_windows
def move_windows_to_new_desktop(num, win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [move_window(i['hWnd'], num) for i in matching_windows]
    return result
def move_windows_to_new_monitor(num, win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [move_window_to_monitor(i['hWnd'], num) for i in matching_windows]
    return result
if __name__ == "__main__":
    cmd_args = sys.argv
    action = cmd_args[cmd_args.index("--action") + 1]
    if action == 'create_desktop': 
        num_of_desktops= cmd_args[cmd_args.index("--numOfNewDesktops") + 1]
        create_new_virtual_desktop(int(num_of_desktops))
    elif action == 'move_window': 
        desktop_num = cmd_args[cmd_args.index("--newDesktop") + 1]
        desktop_num = int(desktop_num)
        win_id = cmd_args[cmd_args.index("--winId") + 1]
        win_id_type = cmd_args[cmd_args.index("--winIdType") + 1]
        move_windows_to_new_desktop(desktop_num, win_id_type, win_id)
    elif action == 'move_virtual_desktop': 
        desktop_num = cmd_args[cmd_args.index("--newDesktop") + 1]
        desktop_num = int(desktop_num)
        move_virtual_desktop(desktop_num)
    elif action == 'move_window_to_monitor': 
        monitor_num = cmd_args[cmd_args.index("--newMonitor") + 1]
        #we expect this input to be 1-indexed
        monitor_num = int(monitor_num) - 1
        win_id = cmd_args[cmd_args.index("--winId") + 1]
        win_id_type = cmd_args[cmd_args.index("--winIdType") + 1]
        move_windows_to_new_monitor(monitor_num, win_id_type, win_id)
    elif action == 'get_monitor_names': 
        app_data_directory = cmd_args[cmd_args.index("--appDataDirectory") + 1]
        get_monitor_names(app_data_directory)
