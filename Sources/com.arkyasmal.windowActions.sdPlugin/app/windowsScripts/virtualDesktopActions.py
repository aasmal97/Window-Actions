from pynput.keyboard import Key, Controller
from getMatchingWindowList import get_matching_windows_list
def create_new_desktop(): 
    keyboard = Controller()
    keyboard.press(Key.cmd)
    keyboard.press(Key.ctrl)
    keyboard.press("d")
    keyboard.release("d")
    keyboard.release(Key.ctrl)
    keyboard.release(Key.cmd)
def move_window(hwnd, num): 
    check_desktops(num)
    window: AppView
    if isinstance(hwnd, int) or isinstance(str): 
        window = AppView(hwnd)
    else: 
        window = AppView.current()
    target_desktop = VirtualDesktop(num)
    window.move(target_desktop)
def move_virtual_desktop(num: int):
    check_desktops(num)
    target_desktop = VirtualDesktop(num)
    target_desktop.go()
    return "Moved to this virtual desktop"

def create_new_virtual_desktop(desktopsToCreate: int, move_to_original: bool = True):
    curr_desktop = VirtualDesktop.current().number
    for x in range(desktopsToCreate):
        create_new_desktop()
    if move_to_original: 
        move_virtual_desktop(curr_desktop)

def check_desktops(num: int, move_to_original: bool = True):
    desktop_available = len(get_virtual_desktops())
    if num > desktop_available:
        diff = num - desktop_available
        create_new_virtual_desktop(diff, move_to_original)

    return f'successfully moved to desktop {num}'
def move_windows_to_new_desktop(num, win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [move_window(i['hWnd'], num) for i in matching_windows]
    return result
def toggle_through_virtual_desktops(curr: -1 or 1): 
    curr_desktop_num = VirtualDesktop.current().number
    if curr == -1 and curr_desktop_num <= 1:
        return VirtualDesktop(1).go()
    if curr == -1:
        return VirtualDesktop(curr_desktop_num - 1).go()
    else:  
        check_desktops(curr_desktop_num + 1, False)
        return VirtualDesktop(curr_desktop_num + 1).go()