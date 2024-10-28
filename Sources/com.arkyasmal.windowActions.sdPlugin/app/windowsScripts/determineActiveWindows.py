# pywintypes import is required or else .exe won't build properly
import pywintypes
import win32gui
import win32process
# import json
import ctypes
from pathlib import Path
import psutil


def get_window_info(hwnd):
    window_text = win32gui.GetWindowText(hwnd)
    if window_text:
        return {'_hWnd': hwnd, 'title': window_text}
    else:
        return None


def get_all_windows():
    """Returns a list of Window objects for all visible windows.
    """
    windowObjs = []
    enumWindows = ctypes.windll.user32.EnumWindows
    enumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    isWindowVisible = ctypes.windll.user32.IsWindowVisible

    def foreach_window(hWnd, lParam):
        if isWindowVisible(hWnd) != 0:
            windowInfo = get_window_info(hWnd)
            if windowInfo != None:
                windowObjs.append(windowInfo)
    enumWindows(enumWindowsProc(foreach_window), 0)
    return windowObjs


def get_all_process():
    processes = [{'ProcessId': proc.pid} for proc in psutil.process_iter(['name', 'pid'])]
    return processes

def get_window_class_names(active_win_data, filter_dup=False):
    win_class_names = [
        {**x, "win_class": win32gui.GetClassName(x["hWnd"])} for x in active_win_data]
    new_map = {}
    new_data = []
    if filter_dup:
        for x in win_class_names:
            win_class = x["win_class"]
            if not win_class in new_map:
                new_data.append(x)
                new_map[win_class] = True
    else:
        new_data = win_class_names
    return new_data


def get_active_windows(
    filter_dup=False
):
    all_process = get_all_process()
    # generate map using PID as key
    process_map = {}
    for x in all_process:
        pid = x["ProcessId"]
        process_map[pid] = x
    # get all active windows
    windows = get_all_windows()
    windows_data = [
        {
            "hWnd": x["_hWnd"], "title": x['title'],
            "pid": win32process.GetWindowThreadProcessId(x["_hWnd"])
        }
        for x in windows
    ]
    new_data = list(filter(lambda x: len(x["title"]) > 0, windows_data))
    for i in range(0, len(new_data)):
        data_pid = new_data[i]["pid"]
        for p in data_pid:
            if str(p) in process_map:
                new_data[i]["program_name"] = process_map[str(p)]["Name"]
                break
    new_data = get_window_class_names(new_data, filter_dup)
    return new_data
