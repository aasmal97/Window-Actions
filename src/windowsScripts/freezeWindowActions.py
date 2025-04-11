import pywintypes
import win32con
from win32api import GetWindowLong, SetWindowLong
from win32gui import SetWindowPos
from getMatchingWindowList import get_matching_windows_list


def freeze_single_window_topmost(hwnd):
    SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                 win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


def unfreeze_single_window(hwnd):
    existing_style = GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    new_style = existing_style & ~win32con.WS_EX_TOPMOST
    SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
    # unfreeze
    SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                 win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    # send to bottom layer
    SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0,
                 win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)


def freeze_windows_topmost(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [freeze_single_window_topmost(
        i['hWnd']) for i in matching_windows]
    return result


def unfreeze_windows_topmost(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [unfreeze_single_window(i['hWnd']) for i in matching_windows]
    return result
