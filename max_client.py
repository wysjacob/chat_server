import json
import time
from ws4py.client.threadedclient import WebSocketClient
import threading
import socket

sockIndex = 0


class CG_Client(WebSocketClient):
    def opened(self):
        print('ws created')

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        print(time.perf_counter())


def create_ws():
    global sockIndex
    print(sockIndex)
    sockIndex += 1
    ws = CG_Client('ws://127.0.0.1:8000/chat')
    ws.connect()
    ws.run_forever()
    print('created')


if __name__ == '__main__':
    times = 600
    threads = []
    for i in range(0, times):
        t = threading.Thread(target=create_ws)
        threads.append(t)
    for i in range(0, times):
        threads[i].start()
    for i in range(0, times):
        threads[i].join()
    print("create success")



