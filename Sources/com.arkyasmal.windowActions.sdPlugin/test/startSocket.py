import asyncio
import websockets
import json
async def delayed_function(websocket):
    reply = {
        "action": "com.arkyasmal.windowActions.onGetMonitorInfo",
        "context": {},
        "payload": {
            "action": "com.arkyasmal.windowActions.onGetMonitorInfo"
        }
        # 'data': {},
        # "targetContext": {}
    }
    await websocket.send(json.dumps(reply))
async def set_interval(func, interval, socket):
    while True:
        await func(socket)
        await asyncio.sleep(interval)
# create handler for each connection
async def handler(websocket, path):
    data = await websocket.recv()
    print(data)
    await set_interval(delayed_function, 5, websocket)
    

start_server = websockets.serve(handler, "localhost", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
