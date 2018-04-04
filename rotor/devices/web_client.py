import time
import asyncio
import websockets
from threading import Thread
import json

class WebClient:

    connections = 0

    def __init__(self, on_message):
        self.on_message = on_message

    @asyncio.coroutine
    def on_connection(self, connection, path):
        self.connections += 1
        while True:
            try:
                str_message = yield from connection.recv()
            except Exception as err:
                self.connections -= 1
                break

            try:
                message = json.loads(str_message)
                self.on_message(message)
            except:
                pass

    def get_connection_count(self):
        return self.connections        

    def run(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            websockets.serve(self.on_connection, '0.0.0.0', 8765))
        loop.run_forever()

    def start(self):
        print("Starting Web Client!")
        loop = asyncio.new_event_loop()
        thread = Thread(target=self.run, args=(loop,))
        thread.start()
