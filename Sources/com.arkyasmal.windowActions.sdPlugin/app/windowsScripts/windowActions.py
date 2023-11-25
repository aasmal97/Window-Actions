#pywintypes import is required or else .exe won't build properly
import pywintypes
import win32con
from win32process import GetWindowThreadProcessId, AttachThreadInput
from win32api import EnumDisplayMonitors, GetMonitorInfo, GetCurrentThreadId
from win32gui import MoveWindow, GetWindowRect, GetWindowPlacement,SetWindowPos, ShowWindow, PostMessage, SetForegroundWindow, GetForegroundWindow, SetActiveWindow, SetFocus
from getMatchingWindowList import get_matching_windows_list
import os
dataDirectory = os.environ['APPDATA']
filePath = os.path.join(dataDirectory, "Elgato\\StreamDeck\\logs\\com.arkyasmal.windowActions.txt")
def focus_single_window(hwnd: str):    
    foregroundWindowHandle = GetForegroundWindow()
    print(foregroundWindowHandle, hwnd)
    if foregroundWindowHandle == hwnd: 
        return
    currentThreadId = GetCurrentThreadId()
    foregroundThreadId = GetWindowThreadProcessId(foregroundWindowHandle)[0]
    AttachThreadInput(currentThreadId, foregroundThreadId, True)
    SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
    SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
    SetActiveWindow(hwnd)
    SetForegroundWindow(hwnd)
    AttachThreadInput(currentThreadId, foregroundThreadId, False)
    ShowWindow(hwnd, win32con.SW_RESTORE)
def resize_single_window(hwnd: str, x, y, width, height, focus: bool):
    focus_param = win32con.SWP_NOZORDER
    if focus: 
        focus_param = win32con.SWP_SHOWWINDOW
        focus_single_window(hwnd)
    SetWindowPos(hwnd,win32con.HWND_TOP,int(x),int(y),int(width),int(height), focus_param)

def err_log(message):
    with open(filePath, "a+") as file:
        file.write(message + "\n")
def determine_placement(hwnd: str):
    placement = GetWindowPlacement(hwnd)
    cmd_show = win32con.SW_NORMAL
    if placement[1] == win32con.SW_SHOWMAXIMIZED:
        cmd_show = win32con.SW_MAXIMIZE
    elif placement[1] == win32con.SW_SHOWMINIMIZED:
        cmd_show = win32con.SW_MINIMIZE
    elif placement[1] == win32con.SW_SHOWNORMAL:
        cmd_show = win32con.SW_SHOWNORMAL
    return cmd_show
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
    #prevent moving window bugs, where window disappears 
    #and becomes transparent
    prev_placement = determine_placement(hwnd)
    ShowWindow(hwnd, win32con.SW_NORMAL)
    MoveWindow(hwnd, monitor_selected[0], monitor_selected[1], new_window_width, new_window_height, True)
    #after movement we restore the previous window state (min, max or normal)
    ShowWindow(hwnd, prev_placement)
    return f'successfully moved to monitor {num}'
def move_windows_to_new_monitor(num, win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [move_window_to_monitor(i['hWnd'], num) for i in matching_windows]
    return result
def minimize_window(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [ShowWindow(i['hWnd'], win32con.SW_MINIMIZE) for i in matching_windows]
    return result
def maximize_window(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [ShowWindow(i['hWnd'], win32con.SW_MAXIMIZE) for i in matching_windows]
    return result
def close_window(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [PostMessage(i['hWnd'], win32con.WM_CLOSE, 0, 0) for i in matching_windows]
    return result
def resize_window(win_id_type, win_id, size: list, coordinates: list, show: bool = True):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    if len(coordinates) != 2:
        coordinates = [0,0]
    x,y = coordinates 
    width, height = size
    result = [resize_single_window(i['hWnd'], x, y, width, height, show) for i in matching_windows]
    return result
def focus_window(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [focus_single_window(i['hWnd']) for i in matching_windows]
    return result