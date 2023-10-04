import json
import os
from determineActiveWindows import get_active_windows, fetch_windows_json
from getMonitorNames import get_monitor_names
from windowActions import move_windows_to_new_monitor, maximize_window, minimize_window, close_window, resize_window
from virtualDesktopActions import create_new_virtual_desktop, move_windows_to_new_desktop, move_virtual_desktop, toggle_through_virtual_desktops
from utilities import one_indexed
dataDirectory = os.environ['APPDATA']
filePath = os.path.join(dataDirectory, "Elgato\\StreamDeck\\Plugins\\com.arkyasmal.windowActions.txt")
def log_event(payload, socket, filePath):
    json_data = {
        "event": "logMessage",
        "payload": {"message": payload} if isinstance(payload, str) else payload,
    }
    new_payload = json.dumps(json_data)
    with open(filePath, "a") as file:
        file.write(new_payload)
    socket.send(new_payload)
def on_active_windows(action, targetContext, customAction, socket, uuid):
    app_data_dir= "Elgato\\StreamDeck\\Plugins\\com.arkyasmal.windowActions.sdPlugin"
    get_active_windows(app_data_dir)
    result = fetch_windows_json(app_data_dir, "activeWindows.json")
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
    socket.send(json.dumps(newEvent))

def on_get_monitor_info(action, targetContext, customAction, socket, uuid):
    app_data_dir= "Elgato\\StreamDeck\\Plugins\\com.arkyasmal.windowActions.sdPlugin"
    get_monitor_names(app_data_dir)
    result = fetch_windows_json(app_data_dir, "activeWindows.json")

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
    socket.send(json.dumps(newEvent))

def parse_event(evt):
    evtObj = json.loads(evt.data)
    targetContext = evtObj["context"]
    payload = evtObj.get("payload", {})
    action = payload.get("action")
    settings = payload.get("settings", {})
    type = settings.get("type")
    name = settings.get("name")
    value = settings.get("value")
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
def respond_to_sub_events(evt, socket, uuid):
    parsedEvent = parse_event(evt)
    action = parsedEvent["action"]
    evtObj = parsedEvent["evtObj"]
    targetContext = parsedEvent["targetContext"]
    if action == "com.arkyasmal.windowActions.on_active_windows":
        on_active_windows(evtObj["action"], targetContext, "com.arkyasmal.windowActions.activeWindows", socket, uuid)
    elif action == "com.arkyasmal.windowActions.on_get_monitor_info":
        on_get_monitor_info(evtObj["action"], targetContext, "com.arkyasmal.windowActions.getmonitorinfo", socket, uuid)
    else:
        log_event("Sub event does not match", socket, filePath)

def respond_to_key_events(evt, socket):
    evt_obj, type, value, name = parse_event(evt)
    # this conditional is here for backwards support for action configured prior
    # to this update
    win_id = value.name if value else name
    match evt_obj.action:
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
                coordinates = [value.coordinates.x, value.coordinates.y] if value.coordinates else [0,0] 
                size = [value.size.width, value.size.height] if value.size else [0,0]
                resize_window(
                    type,
                    win_id,
                    coordinates,
                    size
                )
        case "com.arkyasmal.windowactions.movewindowsvirtual":
            if type and value and win_id and value.newDesktop:
                desktop_num = one_indexed(value.newDesktop)
                move_windows_to_new_desktop(type, win_id, desktop_num)
        case "com.arkyasmal.windowactions.movevirtualdesktops":
            if value and value.newDesktop:
                desktop_num = one_indexed(value.newDesktop)
                move_virtual_desktop(desktop_num)
        case "com.arkyasmal.windowactions.createvirtualdesktops":
            if value and value.numOfDesktopsToCreate:
                create_new_virtual_desktop(int(value.numOfDesktopsToCreate))
        case "com.arkyasmal.windowactions.movewindowstomonitor":
            if type and value and win_id and value.newMonitor:
                move_windows_to_new_monitor(type, win_id, value.newMonitor)
        case "com.arkyasmal.windowactions.movevirtualdesktopright":
            toggle_through_virtual_desktops(1)
        case "com.arkyasmal.windowactions.movevirtualdesktopleft":
            toggle_through_virtual_desktops(-1)
        case _:
            log_event("Button press event does not match", socket, filePath)
            log_event(evt_obj, socket, filePath)

def respond_to_events(evt, socket, uuid):
    action, evt_obj = parse_event(evt)
    if action:
        respond_to_sub_events(evt, socket, uuid)
    elif evt_obj['event'] == "keyDown":
        respond_to_key_events(evt, socket)
        