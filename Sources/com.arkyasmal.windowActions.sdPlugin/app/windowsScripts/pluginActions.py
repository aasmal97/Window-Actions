import sys
from windowActions import move_windows_to_new_monitor
from virtualDesktopActions import create_new_virtual_desktop, move_windows_to_new_desktop, move_virtual_desktop, toggle_through_virtual_desktops
from getMonitorNames import get_monitor_names
if __name__ == "__main__":
    cmd_args = sys.argv
    action = cmd_args[cmd_args.index("--action") + 1]
    if action == 'create_desktop': 
        num_of_desktops= cmd_args[cmd_args.index("--numOfNewDesktops") + 1]
        create_new_virtual_desktop(int(num_of_desktops))
    elif action == 'move_window': 
        desktop_num = cmd_args[cmd_args.index("--newDesktop") + 1]
        desktop_num = int(desktop_num)
        win_id = cmd_args[cmd_args.index("--winId") + 1]
        win_id_type = cmd_args[cmd_args.index("--winIdType") + 1]
        move_windows_to_new_desktop(desktop_num, win_id_type, win_id)
    elif action == 'move_virtual_desktop': 
        desktop_num = cmd_args[cmd_args.index("--newDesktop") + 1]
        #we expect this input to be 1-indexed (so we correct for 0-index)
        desktop_num = int(desktop_num) - 1
        move_virtual_desktop(desktop_num)
    elif action == 'move_window_to_monitor': 
        monitor_num = cmd_args[cmd_args.index("--newMonitor") + 1]
        #we expect this input to be 1-indexed
        monitor_num = int(monitor_num) - 1
        win_id = cmd_args[cmd_args.index("--winId") + 1]
        win_id_type = cmd_args[cmd_args.index("--winIdType") + 1]
        move_windows_to_new_monitor(monitor_num, win_id_type, win_id)
    elif action == 'get_monitor_info': 
        app_data_directory = cmd_args[cmd_args.index("--appDataDirectory") + 1]
        get_monitor_names(app_data_directory)
    elif action == 'move_by_one_virtual_desktop':
        direction = cmd_args[cmd_args.index("--direction") + 1]
        toggle_through_virtual_desktops(int(direction))
