from argparse import ArgumentParser
import json
import websocket
import rel
from handleEvents import respond_to_events
from handleErrs import err_log
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
    err_log(str({
        "inPort": inPort, 
        "inPluginUUID": inPluginUUID, 
        "inRegisterEvent": inRegisterEvent, 
        "inInfo": inInfo
    }))
    try:
        def on_open(ws):
            register_socket(inRegisterEvent)

        def on_message(ws: websocket.WebSocket, message):
            respond_to_events(message, ws, uuid)

        def on_error(ws: websocket.WebSocket, error):
            err_log("Error: " + f"{str(error)}")
        global socket
        global uuid
        uri = "ws://127.0.0.1:" + str(inPort)
        uuid = inPluginUUID
        socket = websocket.WebSocketApp(
            uri, on_open=on_open, on_message=on_message, on_error=on_error)
        socket.run_forever(dispatcher=rel, reconnect=2)
        rel.signal(2, rel.abort)
        rel.dispatch()
    except Exception as e:
        err_log(str(e))


# Main function to be called from the command line
if __name__ == "__main__":
    err_log(str("...starting"))
    try:
        parser = ArgumentParser()
        parser.add_argument("-port", "--port", help="Port number")
        parser.add_argument("-pluginUUID", "--pluginUUID",
                            help="plugin unique id")
        parser.add_argument("-registerEvent", "--registerEvent",
                            help="event needed to register plugin")
        parser.add_argument("-info", "--info", help="StreamDeck device info")
        args = parser.parse_args()
        connectElgatoStreamDeckSocket(
            args.port,
            args.pluginUUID,
            args.registerEvent,
            args.info
        )
        err_log(str("...connected"))
    except Exception as e:
        err_log(str(e))
