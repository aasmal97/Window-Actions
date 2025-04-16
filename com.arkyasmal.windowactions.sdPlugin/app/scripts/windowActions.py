# pywintypes import is required or else .exe won't build properly
import pywintypes
import win32con
from win32gui import SetWindowPos, ShowWindow, PostMessage
from getMatchingWindowList import get_matching_windows_list
from focusWindowAction import focus_single_window


def resize_single_window(hwnd: int | str, x, y, width, height, focus: bool):
    hwnd = int(hwnd)
    focus_param = win32con.SWP_NOACTIVATE
    if focus:
        focus_param = win32con.SWP_SHOWWINDOW
        focus_single_window(hwnd)
        SetWindowPos(hwnd, win32con.HWND_TOP, int(x), int(y),
                     int(width), int(height), focus_param)
    else:
        SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, int(
            x), int(y), int(width), int(height), focus_param)


def minimize_window(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [ShowWindow(i['hWnd'], win32con.SW_MINIMIZE)
              for i in matching_windows]
    return result


def maximize_window(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [ShowWindow(i['hWnd'], win32con.SW_MAXIMIZE)
              for i in matching_windows]
    return result


def close_window(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [PostMessage(i['hWnd'], win32con.WM_CLOSE, 0, 0)
              for i in matching_windows]
    return result


def resize_window(win_id_type, win_id, size: list, coordinates: list, show: bool = True):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    if len(coordinates) != 2:
        coordinates = [0, 0]
    x, y = coordinates
    width, height = size
    result = [resize_single_window(
        i['hWnd'], x, y, width, height, show) for i in matching_windows]
    return result
