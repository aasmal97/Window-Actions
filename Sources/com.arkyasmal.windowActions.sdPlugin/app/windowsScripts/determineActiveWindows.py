import pyautogui
import win32gui
import win32process
import os
import csv
import json
from pathlib import Path
import sys
def get_all_process(): 
    all_processes = os.popen("wmic process get name, processid /format:csv").read()
    all_processes_split = all_processes.split("\n")
    all_processes_split = list(filter(lambda x: x !='', all_processes_split))
    reader = csv.DictReader(all_processes_split, delimiter=',')
    all_processes_list = list(reader)
    return all_processes_list
def get_window_class_names(active_win_data, filter_dup=False): 
    win_class_names = [{**x, "win_class": win32gui.GetClassName(x["hWnd"])} for x in active_win_data]
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
def create_json_file(active_win_data, app_data_directory):
    new_data_json = json.dumps(active_win_data)
    directory_path = Path(f'{os.getenv("APPDATA")}\\{app_data_directory}')
    if not directory_path.exists():
        os.makedirs(directory_path)
    path_to_file = directory_path / 'activeWindows.json'
    path_to_file = path_to_file.resolve()
    try:
        f = open(path_to_file, "x")
        f.write(new_data_json)
        return new_data_json
    except FileExistsError:
        f = open(path_to_file, "w")
        f.write(new_data_json)
        return new_data_json
    except: 
        print("An error occured")
def get_active_windows(app_data_directory, filter_dup = False):
    all_process = get_all_process()
    #generate map using PID as key
    process_map = {}
    for x in all_process: 
        pid = x["ProcessId"]
        process_map[pid] = x
    # get all active windows
    windows = pyautogui.getAllWindows()
    windows_data=[
        {
            "hWnd": x._hWnd, "title": x.title, 
            "pid": win32process.GetWindowThreadProcessId(x._hWnd)
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
    create_json_file(new_data, app_data_directory)
    return new_data
    
if __name__ == "__main__":
    cmd_args = sys.argv
    active_windows= []
    app_data_directory = cmd_args[cmd_args.index("--appDataDirectory") + 1]
    if "--filterDup" in cmd_args: 
        active_windows = get_active_windows(app_data_directory, True) 
    else:
        active_windows = get_active_windows(app_data_directory, False)
    print(active_windows)
