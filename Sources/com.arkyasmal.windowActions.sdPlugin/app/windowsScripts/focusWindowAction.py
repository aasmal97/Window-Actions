#pywintypes import is required or else .exe won't build properly
import pywintypes
import ctypes
import win32con
from win32process import GetWindowThreadProcessId, AttachThreadInput
from win32api import GetCurrentThreadId
from win32gui import SetWindowPos, ShowWindow, SetForegroundWindow, GetForegroundWindow, SetActiveWindow
from getMatchingWindowList import get_matching_windows_list
user32 = ctypes.windll.user32
#focuses on new window, and returns the previous focused window
def focus_single_window(hwnd: str):    
    foregroundWindowHandle = GetForegroundWindow()
    if foregroundWindowHandle == hwnd: 
        return hwnd
    currentThreadId = GetCurrentThreadId()
    foregroundThreadId = GetWindowThreadProcessId(foregroundWindowHandle)[0]
    AttachThreadInput(currentThreadId, foregroundThreadId, True)
    SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
    SetActiveWindow(hwnd)
    SetForegroundWindow(hwnd)
    AttachThreadInput(currentThreadId, foregroundThreadId, False)
    if user32.IsZoomed(hwnd):
        ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
    else:
        ShowWindow(hwnd, win32con.SW_RESTORE) 
    return foregroundWindowHandle
def focus_windows(win_id_type, win_id):
    matching_windows = get_matching_windows_list(win_id_type, win_id)
    result = [focus_single_window(i['hWnd']) for i in matching_windows]
    return result
