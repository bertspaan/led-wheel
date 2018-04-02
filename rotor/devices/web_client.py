import time
import asyncio
import websockets
from threading import Thread

class WebClient:

    async def message(self, websocket, path):
        async for message in websocket:
            print(message)

    def run(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            websockets.serve(self.message, 'localhost', 8765))
        loop.run_forever()

    def start(self):
        print("Starting Web Client!")
        loop = asyncio.new_event_loop()
        thread = Thread(target=self.run, args=(loop,))
        thread.start()
