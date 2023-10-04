from pynput.keyboard import Key, Controller
from getMatchingWindowList import get_matching_windows_list
from virtualDesktopDLLFile import get_build_num, initialize_app_view
app_instance = initialize_app_view()
def create_new_desktop(): 
    [build,_] = get_build_num()
    if(build>22000): 
        return app_instance.CreateDesktop()
    keyboard = Controller()
    keyboard.press(Key.cmd)
    keyboard.press(Key.ctrl)
    keyboard.press("d")
    keyboard.release("d")
    keyboard.release(Key.ctrl)
    keyboard.release(Key.cmd)
def move_window(hwnd, num): 
    check_desktops(num=num)
    app_instance.MoveWindowToDesktopNumber(hwnd, num)
def move_windows_to_new_desktop(num, win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [move_window(i['hWnd'], num) for i in matching_windows]
    return result
def move_virtual_desktop(num: int):
    check_desktops(num)
    app_instance.GoToDesktopNumber(num)
    return "Moved to this virtual desktop"

def create_new_virtual_desktop(desktopsToCreate: int, move_to_original: bool = True):
    curr_desktop = app_instance.GetCurrentDesktopNumber()
    for x in range(desktopsToCreate):
        create_new_desktop()
    if move_to_original: 
        move_virtual_desktop(curr_desktop)

def check_desktops(num: int, move_to_original: bool = True):
    desktop_available = app_instance.GetDesktopCount()
    print(desktop_available, num, move_to_original)
    if num > desktop_available:
        diff = num - desktop_available
        create_new_virtual_desktop(diff, move_to_original)
    return f'successfully moved to desktop {num}'

def toggle_through_virtual_desktops(curr: -1 or 1):
    curr_desktop_num = app_instance.GetCurrentDesktopNumber()
    if curr == -1 and curr_desktop_num <= 1:
        return app_instance.GoToDesktopNumber(0)
    if curr == -1:
        return app_instance.GoToDesktopNumber(curr_desktop_num - 1)
    else:  
        check_desktops(curr_desktop_num + 2, False)
        return app_instance.GoToDesktopNumber(curr_desktop_num + 1)
