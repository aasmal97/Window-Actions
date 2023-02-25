from pyvda import AppView, VirtualDesktop, get_virtual_desktops
from determineActiveWindows import get_active_windows
import sys
import re
from pynput.keyboard import Key, Controller
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
    result = [move_window(i['hWnd'], num) for i in matching_windows]
    return result
if __name__ == "__main__":
    cmd_args = sys.argv
    action = cmd_args[cmd_args.index("--action") + 1]
    if action == 'create_desktop': 
        num_of_desktops= cmd_args[cmd_args.index("--numOfNewDesktops") + 1]
        create_new_virtual_desktop(int(num_of_desktops))
    desktop_num = cmd_args[cmd_args.index("--newDesktop") + 1]
    desktop_num = int(desktop_num)
    if action == 'move_window': 
        win_id = cmd_args[cmd_args.index("--winId") + 1]
        win_id_type = cmd_args[cmd_args.index("--winIdType") + 1]
        move_windows_to_new_desktop(desktop_num, win_id_type, win_id)
    elif action == 'move_virtual_desktop': 
        move_virtual_desktop(desktop_num)
