from argparse import ArgumentParser
import json
import websocket
import rel
from handle_events import respond_to_events, filePath
socket = None
uuid = None
def err_log(message):
    with open(filePath, "a+") as file:
        file.write(message + "\n")

def register_socket(inRegisterEvent):
    try:
        event = json.loads(inRegisterEvent)
    except:
        event = inRegisterEvent
        
    registerData = {
        "event": event,
        "uuid": uuid
    }
    
    socket.send(json.dumps(registerData))

def connectElgatoStreamDeckSocket(inPort, inPluginUUID, inRegisterEvent, inInfo):
    def on_open(ws):
        register_socket(inRegisterEvent)
    def on_message(ws,message):
        err_log("socket to respond to event")
        respond_to_events(message, ws, uuid)
        err_log("socket responded to event")
    def on_error(ws, error):
        err_log(str(error))
    global socket
    global uuid
    uri = "ws://127.0.0.1:" + str(inPort)
    uuid = inPluginUUID
    socket = websocket.WebSocketApp(uri, on_open=on_open, on_message=on_message, on_error=on_error)
    socket.run_forever(dispatcher=rel, reconnect=2)
    rel.signal(2, rel.abort)
    rel.dispatch()


# Main function to be called from the command line
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-port", "--port", help="Port number")
    parser.add_argument("-pluginUUID", "--pluginUUID", help="plugin unique id")
    parser.add_argument("-registerEvent", "--registerEvent", help="event needed to register plugin")
    parser.add_argument("-info", "--info", help="StreamDeck device info")
    args = parser.parse_args()
    connectElgatoStreamDeckSocket(
        args.port,
        args.pluginUUID,
        args.registerEvent,
        args.info
    )
