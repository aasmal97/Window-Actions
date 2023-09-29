# from pyvda import AppView, VirtualDesktop, get_virtual_desktops
# import sys
# import functools
# import os
# import json
import win32con
import pywintypes
from win32api import EnumDisplayMonitors, GetMonitorInfo, EnumDisplayDevices
from win32gui import MoveWindow, GetWindowRect, GetWindowPlacement, ShowWindow
# from win32com.client import GetObject
# from pynput.keyboard import Key, Controller
# from difflib import SequenceMatcher
# from pathlib import Path
from getMatchingWindowList import get_matching_windows_list
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