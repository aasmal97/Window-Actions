# pywintypes import is required or else .exe won't build properly
import pywintypes
import win32gui
import win32process
# import json
import psutil
from handleErrs import err_log


def get_window_info(hwnd: int | str):
    window_text = win32gui.GetWindowText(int(hwnd))
    if window_text:
        return {'_hWnd': hwnd, 'title': window_text}
    else:
        return None


def get_all_windows():
    # """Returns a list of Window objects for all visible windows.
    # """
    windowObjs = []

    def enum_windows_callback(hwnd, _):
        # """Callback function for EnumWindows."""
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                windowObjs.append({
                    "_hWnd": hwnd,
                    "title": win32gui.GetWindowText(hwnd),
                    "process_name": process.name(),
                    "pid": pid
                })
            except psutil.NoSuchProcess:
                pass
        return True

    win32gui.EnumWindows(enum_windows_callback, None)

    return windowObjs


def get_all_process():
    processes = [{'ProcessId': proc.pid, "Name": proc.name()}
                 for proc in psutil.process_iter(['name', 'pid'])]
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
        pid = str(x["ProcessId"])
        process_map[pid] = x
    # get all active windows
    windows = get_all_windows()
    windows_data = [
        {
            "hWnd": int(x["_hWnd"]), "title": x['title'],
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

# Grab windows, but failed in contained environment with cx_Freeze. Very unreliable
    # enumWindows = ctypes.windll.user32.EnumWindows
    # enumWindowsProc = ctypes.WINFUNCTYPE(
    #     ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    # isWindowVisible = ctypes.windll.user32.IsWindowVisible

    # def foreach_window(hWnd: str | int, lParam):
    #     if isWindowVisible(hWnd) != 0:
    #         windowInfo = get_window_info(int(hWnd))
    #         if windowInfo != None:
    #             windowObjs.append(windowInfo)
    # enumWindows(enumWindowsProc(foreach_window), 0)

    # err_log(str(windowObjs))
    # err_log(str(enumWindows))
    # err_log(str(
    #     enumWindowsProc))
    # err_log(str(isWindowVisible))
    # err_log(str(windowObjs))
