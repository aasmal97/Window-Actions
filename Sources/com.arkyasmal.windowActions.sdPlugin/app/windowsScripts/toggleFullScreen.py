import pywintypes
import ctypes
import win32con
from pynput.keyboard import Key, Controller
from win32api import GetMonitorInfo, SetWindowLong, MonitorFromWindow, GetWindowLong, SendMessage
from win32gui import SetWindowPos, ShowWindow, GetWindowRect
from focusWindow import focus_single_window
user32 = ctypes.windll.user32
currFullScreenWindows = {}
def fullscreen_on(hwnd: str):
    #store window styles and size
    is_maximized = user32.IsZoomed(hwnd)
    windowRect = GetWindowRect(hwnd)
    if is_maximized:
        SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    #Show the window
    ShowWindow(hwnd, win32con.SW_SHOW); 
    if hwnd in currFullScreenWindows:
        currFullScreenWindows[hwnd]["fullscreen"] = False
        currFullScreenWindows[hwnd]["windowRect"] = windowRect
    # Create new data map
    else:
        currFullScreenWindows[hwnd] = {
            "windowStyles": GetWindowLong(hwnd, win32con.GWL_STYLE),
            "extendedWindowStyles": GetWindowLong(hwnd, win32con.GWL_EXSTYLE),
            "windowRect": windowRect,
            "fullscreen": False,
            'isMaximized': is_maximized,
        }
    windowStyles = currFullScreenWindows[hwnd]["windowStyles"]
    extendedWindowStyles = currFullScreenWindows[hwnd]["extendedWindowStyles"]
    monitorInfo = GetMonitorInfo(MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST))["Monitor"]
    # Set the window styles
    SetWindowLong(hwnd, win32con.GWL_STYLE, windowStyles & ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME))
    #Set the extended window styles
    SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        extendedWindowStyles & ~(win32con.WS_EX_DLGMODALFRAME | win32con.WS_EX_WINDOWEDGE | win32con.WS_EX_CLIENTEDGE | win32con.WS_EX_STATICEDGE)
    )
    # Resize, move, and refresh the window
    SetWindowPos (
        hwnd,
        None,
        monitorInfo[0], monitorInfo[1], 
        monitorInfo[2] - monitorInfo[0],
        monitorInfo[3] - monitorInfo[1],
        win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_FRAMECHANGED
    )
    # Indicate that fullscreen is on
    currFullScreenWindows[hwnd]["fullscreen"] = True; 
def fullscreen_off(hwnd: str):
    #Set the window styles
    windowStyles = currFullScreenWindows[hwnd]["windowStyles"]
    extendedWindowStyles = currFullScreenWindows[hwnd]["extendedWindowStyles"]
    windowRect = currFullScreenWindows[hwnd]["windowRect"]
    is_maximized = currFullScreenWindows[hwnd]["isMaximized"]
    SetWindowLong(hwnd, win32con.GWL_STYLE, windowStyles); 
    # Set the extended window styles
    SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extendedWindowStyles); 
    #Resize, move, and refresh the window
    SetWindowPos 
    (
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
    currFullScreenWindows[hwnd]["fullscreen"] = False; 
def toggle_fullscreen_with_keys(hwnd: str): 
    prev_hwnd = focus_single_window(hwnd)
    keyboard = Controller()
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)
    # return focus to previous window
    focus_single_window(prev_hwnd)
def toggle_fullscreen(hwnd: str):
    fullscreen = currFullScreenWindows[hwnd]["fullscreen"] if hwnd in currFullScreenWindows else False
    if not fullscreen:
        #call direct window size manipulation function
        fullscreen_on(hwnd)
    else:
        #untoggle direct window size manipulation function
        fullscreen_off(hwnd)
    toggle_fullscreen_with_keys(hwnd)
    return currFullScreenWindows[hwnd]