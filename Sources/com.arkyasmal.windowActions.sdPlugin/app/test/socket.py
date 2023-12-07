import asyncio
import websockets
import json
 
# create handler for each connection
async def handler(websocket, path):
    data = await websocket.recv()
    reply = {}
    print(data)
    await websocket.send(json.dumps(reply))

start_server = websockets.serve(handler, "localhost", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
