from pyvda import AppView, VirtualDesktop
import sys
from determineActiveWindows import get_active_windows
import os
import re
def move_virtual_desktop(num):
    target_desktop = VirtualDesktop(num)
    target_desktop.go()
    return "Moved to this virtual desktop"
def move_window(hwnd, num): 
    window: AppView
    if isinstance(hwnd, str): 
        window = AppView(hwnd)
    else: 
        window = AppView.current()
    target_desktop = VirtualDesktop(num)
    window.move(target_desktop)
    return f'successfully moved to desktop {num}'
def test_regex(pattern, testStr): 
    return re.search(pattern, testStr)
def move_windows_to_new_desktop(num, win_id_type, win_id):
    id_type = "title" if win_id_type == 'win_title' or win_id_type == 'win_ititle' else win_id_type
    is_partial_str = win_id_type == 'win_ititle'
    data_directory = os.getenv('APPDATA')
    file_path = os.path.join( data_directory,"Elgato\\StreamDeck\\Plugins\\com.arkyasmal.windowActions.txt")
    all_windows = get_active_windows(file_path)
    matching_windows = filter(lambda window: test_regex(window[id_type], win_id) if is_partial_str else window[id_type] == win_id, all_windows)
    result =  [move_window(i.hWnd, num) for i in matching_windows]
    return result
if __name__ == "__main__":
    cmd_args = sys.argv
    desktop_num = cmd_args[cmd_args.index("--newDesktop") + 1]
    win_id_type = cmd_args[cmd_args.index("--winId") + 1]
    win_id = cmd_args[cmd_args.index("--winIdType") + 1]
    action = cmd_args[cmd_args.index("--action") + 1]
    if action == 'move_window': 
        move_windows_to_new_desktop(desktop_num, win_id_type, win_id)
    elif action == 'move_virtual_desktop': 
        move_virtual_desktop(desktop_num)
