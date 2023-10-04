import argparse
from argparse import ArgumentParser
import json
import websocket
import rel
from handle_events import respond_to_events
websocket.enableTrace(True)
parser = ArgumentParser()
args = parser.parse_args()
socket = None
uuid = None


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
    def on_open():
        register_socket(inRegisterEvent)
    def on_message(message):
        respond_to_events(message, socket, uuid)
    global socket
    global uuid
    uri = "ws://127.0.0.1:" + str(inPort)
    uuid = inPluginUUID
    socket = websocket.WebSocketApp(uri, on_open=on_open, on_message=on_message, on_close=lambda: None)
    socket.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()
# Main function to be called from the command line
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", "--port", type=int, help="Port number")
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
