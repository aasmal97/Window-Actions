from pyvda import AppView, VirtualDesktop
from determineActiveWindows import get_active_windows
import sys
import os
import re
def move_virtual_desktop(num):
    target_desktop = VirtualDesktop(num)
    target_desktop.go()
    return "Moved to this virtual desktop"
def move_window(hwnd, num): 
    window: AppView
    if isinstance(hwnd, int) or isinstance(str): 
        window = AppView(hwnd)
    else: 
        window = AppView.current()
    target_desktop = VirtualDesktop(num)
    window.move(target_desktop)
    return f'successfully moved to desktop {num}'
def test_regex(pattern, testStr):
    result = re.search(pattern, testStr)
    return result
def move_windows_to_new_desktop(num, win_id_type, win_id):
    id_type = "title" if win_id_type == 'win_title' or win_id_type == 'win_ititle' else win_id_type
    is_partial_str = win_id_type == 'win_ititle'
    file_path = "Elgato\StreamDeck\Plugins\com.arkyasmal.windowActions.txt"
    all_windows = get_active_windows(app_data_directory = file_path)
    matching_windows_itr = filter(lambda window: test_regex(win_id, window[id_type]) if is_partial_str else window[id_type] == win_id, all_windows)
    matching_windows = list(matching_windows_itr)
    print(matching_windows)
    result = [move_window(i['hWnd'], num) for i in matching_windows]
    return result
if __name__ == "__main__":
    cmd_args = sys.argv
    action = cmd_args[cmd_args.index("--action") + 1]
    desktop_num = cmd_args[cmd_args.index("--newDesktop") + 1]
    desktop_num = int(desktop_num)
    if action == 'move_window': 
        win_id = cmd_args[cmd_args.index("--winId") + 1]
        win_id_type = cmd_args[cmd_args.index("--winIdType") + 1]
        move_windows_to_new_desktop(desktop_num, win_id_type, win_id)
    elif action == 'move_virtual_desktop': 
        move_virtual_desktop(desktop_num)
