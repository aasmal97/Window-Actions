import json
import os
from determineActiveWindows import get_active_windows
from getMonitorNames import get_monitor_names
from windowActions import move_windows_to_new_monitor, maximize_window, minimize_window, close_window, resize_window, freeze_windows_topmost, unfreeze_windows_topmost, focus_windows
from virtualDesktopActions import create_new_virtual_desktop, move_windows_to_new_desktop, move_virtual_desktop, toggle_through_virtual_desktops
from utilities import one_indexed
import websocket
dataDirectory = os.environ['APPDATA']
filePath = os.path.join(dataDirectory, r"Elgato\StreamDeck\logs\com.arkyasmal.windowActions\error.txt")
def create_file_with_directories(path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, "w")
        file.close()
        print("File created successfully!")
    except Exception as e:
        print(str(e))
def write_to_file(message):
     with open(filePath, "a+") as file:
            file.write(message + "\n")
def err_log(message):
    try:
        write_to_file(message)
    except FileNotFoundError as e:
        create_file_with_directories(filePath)
        write_to_file(message)
def log_event(payload, socket, filePath):
    json_data = {
        "event": "logMessage",
        "payload": {"message": payload} if isinstance(payload, str) else payload,
    }
    new_payload = json.dumps(json_data)
    with open(filePath, "a+") as file:
        file.write(new_payload)
    socket.send(new_payload)
def on_active_windows(action, targetContext, customAction, socket: websocket.WebSocket, uuid):
    result = get_active_windows()
    newEvent = {
        "action": action,
        "event": "sendToPropertyInspector",
        "context": targetContext,
        "payload": {
            "action": customAction,
            "result": result,
            "targetContext": uuid
        }
    }
    print(newEvent, 'active windows')
    socket.send(json.dumps(newEvent))
def on_get_monitor_info(action, targetContext, customAction, socket: websocket.WebSocket, uuid):
    result = get_monitor_names()
    newEvent = {
        "action": action,
        "event": "sendToPropertyInspector",
        "context": targetContext,
        "payload": {
            "action": customAction,
            "result": result,
            "targetContext": uuid
        }
    }
    print(newEvent, 'monitor names')
    socket.send(json.dumps(newEvent))
def parse_event(evt):
    evtObj = evt.get("data", evt)
    targetContext = evtObj.get("context", {})
    payload = evtObj.get("payload", {}) 
    action = payload.get('action', '')
    settings = payload.get("settings", {})
    type = settings.get("type", '')
    name = settings.get("name", '')
    value = settings.get("value", '')
    return {
        "targetContext": targetContext,
        "payload": payload,
        "action": action,
        "settings": settings,
        "type": type,
        "value": value,
        "name": name,
        "evtObj": evtObj
    }
def respond_to_sub_events(evt, socket: websocket.WebSocket, uuid):
    parsedEvent = parse_event(evt)
    action = parsedEvent["action"]
    evtObj = parsedEvent["evtObj"]
    targetContext = parsedEvent["targetContext"]
    if action == "com.arkyasmal.windowActions.onActiveWindows":
        on_active_windows(evtObj["action"], targetContext, "com.arkyasmal.windowActions.activeWindows", socket, uuid)
    elif action == "com.arkyasmal.windowActions.onGetMonitorInfo":
        on_get_monitor_info(evtObj["action"], targetContext, "com.arkyasmal.windowActions.getmonitorinfo", socket, uuid)
    else:
        log_event("Sub event does not match", socket, filePath)
def respond_to_key_events(evt, socket: websocket.WebSocket):
    evt_dict = parse_event(evt)
    evt_obj, type, value, name = evt_dict["evtObj"], evt_dict["type"], evt_dict["value"], evt_dict["name"]
    # this conditional is here for backwards support for action configured prior
    # to this update
    win_id = value.get('name', '') if value else name
    match evt_obj.get("action", ''):
        case "com.arkyasmal.windowactions.minimizewindows":
            if type and win_id:
                minimize_window(type, win_id)
        case "com.arkyasmal.windowactions.maximizewindows":
            if type and win_id:
                maximize_window(type, win_id)
        case "com.arkyasmal.windowactions.closewindows":
            if type and win_id:
                close_window(type, win_id)
        case "com.arkyasmal.windowactions.resizewindows":
            if type and win_id and value:
                    autofocus = value.get('autoFocus', None) if value.get('autoFocus', None) == False else True
                    coordinates = [value['coordinates']['x'], value['coordinates']['y']] if value.get('coordinates', None) else [0,0] 
                    size = [value['size']['width'], value['size']['height']] if value.get('size', None) else [0,0]
                    resize_window(
                        type,
                        win_id,
                        size,
                        coordinates,
                        autofocus
                    )
        case "com.arkyasmal.windowactions.focuswindow":
            if type and win_id:
                focus_windows(type, win_id)
        case "com.arkyasmal.windowactions.lockwindowtopmost": 
            if type and win_id:        
                freeze_windows_topmost(type, win_id)
        case "com.arkyasmal.windowactions.unlockwindowtopmost":
            if type and win_id:
                unfreeze_windows_topmost(type, win_id)
        case "com.arkyasmal.windowactions.movewindowsvirtual":
            if type and value and win_id and value.get('newDesktop', 0):
                desktop_num = one_indexed(value.get('newDesktop', 0))
                move_windows_to_new_desktop(desktop_num,type, win_id)
        case "com.arkyasmal.windowactions.movevirtualdesktops":
            if value and value.get('newDesktop', 0):
                desktop_num = one_indexed(value.get('newDesktop', 0))
                move_virtual_desktop(desktop_num)
        case "com.arkyasmal.windowactions.createvirtualdesktops":
            if value and value.get('numOfDesktopsToCreate', 0):
                create_new_virtual_desktop(int(value.get('numOfDesktopsToCreate', 0)))
        case "com.arkyasmal.windowactions.movewindowstomonitor":
            if type and value and win_id and value.get('newMonitor', 0):
                monitor_num = one_indexed(value.get('newMonitor', 1))
                move_windows_to_new_monitor(monitor_num,type, win_id)
        case "com.arkyasmal.windowactions.movevirtualdesktopright":
            toggle_through_virtual_desktops(1)
        case "com.arkyasmal.windowactions.movevirtualdesktopleft":
            toggle_through_virtual_desktops(-1)
        case _:
            log_event("Button press event does not match", socket, filePath)
            log_event(evt_obj, socket, filePath)
def respond_to_events(evt, socket:websocket.WebSocket, uuid):
    evt_dict = json.loads(evt)
    try:
        evt_obj = parse_event(evt_dict)
        action, evt_obj = evt_obj["action"], evt_obj["evtObj"]
        if action:
            respond_to_sub_events(evt_dict, socket, uuid)
        elif evt_obj.get('event', '') == "keyDown":
            respond_to_key_events(evt_dict, socket)
    except Exception as e:
        err_log(str(e))