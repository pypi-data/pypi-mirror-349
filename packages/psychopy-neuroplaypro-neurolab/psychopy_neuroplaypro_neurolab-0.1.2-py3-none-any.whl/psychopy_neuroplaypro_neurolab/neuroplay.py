# neuroplay.py (в корне плагина)

__all__ = ['NeuroPlayProClient']

import websocket
import threading
import json
import time


class NeuroPlayProClient:
    def __init__(self, url="ws://localhost:11234"):
        self.url = url
        self.ws = None
        self.running = False
        self.listen_thread = None
        self.messages = []

    def connect(self):
        self.ws = websocket.create_connection(self.url)

    def send_marker(self, label="TRIGGER"):
        self.ws.send(json.dumps({"marker": label}))

    def close(self):
        if self.ws:
            self.ws.close()

    def listen(self):
        self.running = True

        def loop():
            while self.running:
                try:
                    msg = self.ws.recv()
                    self.messages.append(msg)
                except:
                    self.running = False

        self.listen_thread = threading.Thread(target=loop)
        self.listen_thread.start()

    def stop(self):
        self.running = False
        if self.listen_thread:
            self.listen_thread.join()
