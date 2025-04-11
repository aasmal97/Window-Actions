import pywintypes
import ctypes
import win32con
import os
from pynput.keyboard import Key, Controller
from win32api import GetMonitorInfo, SetWindowLong, MonitorFromWindow, GetWindowLong
from win32gui import SendMessage, SetWindowPos, GetWindowRect
from focusWindowAction import focus_single_window
from getMatchingWindowList import get_matching_windows_list
from determineActiveWindows import get_active_windows
import time
import json
user32 = ctypes.windll.user32
dataDirectory = os.environ['APPDATA']
filePath = os.path.join(
    dataDirectory, r"Elgato\StreamDeck\Plugins\com.arkyasmal.windowactions.sdPlugin\currFullScreenWindows.json")


def load_fullscreen_windows_from_file():
    try:
        with open(filePath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        file = open(filePath, "w+")
        file.close()
        return {}
    except Exception as e:
        print(str(e))
        return {}


def fullscreen_on(hwnd: int | str, currFullScreenWindows: dict):
    hwnd = int(hwnd)
    # store window styles and size
    is_maximized = user32.IsZoomed(int(hwnd))
    windowRect = GetWindowRect(hwnd)
    if is_maximized:
        SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    currFullScreenWindows[hwnd] = {
        "windowStyles": GetWindowLong(hwnd, win32con.GWL_STYLE),
        "extendedWindowStyles": GetWindowLong(hwnd, win32con.GWL_EXSTYLE),
        "windowRect": windowRect,
        "fullscreen": False,
        'isMaximized': is_maximized,
    }
    windowStyles = currFullScreenWindows[hwnd]["windowStyles"]
    extendedWindowStyles = currFullScreenWindows[hwnd]["extendedWindowStyles"]
    monitorInfo = GetMonitorInfo(MonitorFromWindow(
        hwnd, win32con.MONITOR_DEFAULTTONEAREST))["Monitor"]
    # Set the window styles
    SetWindowLong(hwnd, win32con.GWL_STYLE, windowStyles & ~
                  (win32con.WS_CAPTION | win32con.WS_THICKFRAME))
    # Set the extended window styles
    SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        extendedWindowStyles & ~(win32con.WS_EX_DLGMODALFRAME | win32con.WS_EX_WINDOWEDGE |
                                 win32con.WS_EX_CLIENTEDGE | win32con.WS_EX_STATICEDGE)
    )
    # Resize, move, and refresh the window
    SetWindowPos(
        hwnd,
        None,
        monitorInfo[0], monitorInfo[1],
        monitorInfo[2] - monitorInfo[0],
        monitorInfo[3] - monitorInfo[1],
        win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_FRAMECHANGED
    )
    # Indicate that fullscreen is on
    currFullScreenWindows[hwnd]["fullscreen"] = True


def fullscreen_off(hwnd: int | str , currFullScreenWindows: dict):
    hwnd = int(hwnd)
    # Set the window styles
    windowStyles = currFullScreenWindows[hwnd]["windowStyles"]
    extendedWindowStyles = currFullScreenWindows[hwnd]["extendedWindowStyles"]
    windowRect = currFullScreenWindows[hwnd]["windowRect"]
    is_maximized = currFullScreenWindows[hwnd]["isMaximized"]
    SetWindowLong(hwnd, win32con.GWL_STYLE, windowStyles)
    # Set the extended window styles
    SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extendedWindowStyles)
    # Resize, move, and refresh the window
    SetWindowPos(
        hwnd,
        None,
        windowRect[0], windowRect[1],
        windowRect[2] - windowRect[0],
        windowRect[3] - windowRect[1],
        win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_FRAMECHANGED
    )
    if is_maximized:
        SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
    # Indicate that fullscreen is off
    currFullScreenWindows[hwnd]["fullscreen"] = False


def fullscreen_key_commands():
    keyboard = Controller()
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)


def toggle_fullscreen_with_keys(hwnd: int | str):
    hwnd = int(hwnd)
    # ensure synchronous execution
    prev_hwnd = None
    try:
        prev_hwnd = focus_single_window(hwnd)
        fullscreen_key_commands()
    finally:
        if prev_hwnd:
            # ensure app updates. This can be improved/optimized
            # by re-factoring focus_single_window to recieve a message that
            # confirms the window has been re-painted
            # but it is unneccessary for most modern machines,
            # as focusing a window usually occurs in less than
            # 1/3 of a second. For now, this is good enough
            time.sleep(0.2)
            focus_single_window(prev_hwnd)


def toggle_fullscreen(hwnd: int | str, currFullScreenWindows: dict):
    # load data into dict
    fullscreen = currFullScreenWindows[hwnd]["fullscreen"] if hwnd in currFullScreenWindows else False
    if not fullscreen:
        # call direct window size manipulation function
        fullscreen_on(hwnd, currFullScreenWindows)
    else:
        # untoggle direct window size manipulation function
        fullscreen_off(hwnd, currFullScreenWindows)
    toggle_fullscreen_with_keys(hwnd)
    return currFullScreenWindows[hwnd]


def cleanup_windows(currFullScreenWindows: dict):
    active_windows = get_active_windows()
    active_windows_dict = {str(i['hWnd']): i for i in active_windows}
    curr_windows_list = list(currFullScreenWindows.keys())
    for i in curr_windows_list:
        if i not in active_windows_dict:
            del currFullScreenWindows[i]


def toggle_fullscreen_windows(win_id_type: str, win_id: str):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    currFullScreenWindows = load_fullscreen_windows_from_file()
    # clean up any data from window handles that don't exist
    cleanup_windows(currFullScreenWindows)
    # activate fullscreen
    result = [toggle_fullscreen(i['hWnd'], currFullScreenWindows)
              for i in matching_windows]
    # save data to file
    with open(filePath, "w") as file:
        json.dump(currFullScreenWindows, file)
    return result
