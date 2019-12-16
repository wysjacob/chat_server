import json
import logging
import uuid
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.resource import Resource, WebSocketApplication
import redis
import multiprocessing
import threading


class MemoryBroker():
    def __init__(self):
        self.sockets = {}
        self.pool = redis.ConnectionPool(host="127.0.0.1", port=6379, max_connections=1024)
        self.conn = redis.Redis(connection_pool=self.pool)

    def subscribe(self, key, socket):
        if key not in self.sockets:
            self.sockets[key] = set()

        if socket in self.sockets[key]:
            return

        self.sockets[key].add(socket)

    def publish(self, key, data):
        self.conn.publish(key, json.dumps(data))

    def unsubscribe(self, key, socket):
        if key not in self.sockets:
            return
        self.sockets[key].remove(socket)


def subscriber(broker: MemoryBroker):

    ps = broker.conn.pubsub()
    ps.subscribe("room1")
    for obj in ps.listen():
        if obj['type'] == "message":
            data = obj['data'].decode("UTF-8")
            if broker.sockets:
                for ws in broker.sockets['room1']:
                    ws.on_broadcast(json.loads(data))
        elif obj['type'] == "subscribe":
            print("线程：%s 消息已订阅." % (multiprocessing.current_process().pid))


def sub(broker):

    thread = threading.Thread(name="sub_thread", target=subscriber, args=(broker,))
    thread.start()


broker = MemoryBroker()
sub(broker)


class Chat(WebSocketApplication):
    def on_open(self, *args, **kwargs):
        self.userid = uuid.uuid4()
        broker.subscribe('room1', self)

    def on_close(self, *args, **kwargs):
        broker.unsubscribe('room1', self)

    def on_message(self, message, *args, **kwargs):
        if not message:
            return
        data = json.loads(message)
        data['user'] = self.userid.hex
        broker.publish('room1', data)

    def on_broadcast(self, data):
        self.ws.send(json.dumps(data))


def index(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    html = open('index.html', 'rb').read()
    return [html]


application = Resource([
    ('^/chat', Chat),
    ('^/', index)
])


if __name__ == '__main__':
    WSGIServer('{}:{}'.format('0.0.0.0', 8000), application, handler_class=WebSocketHandler).serve_forever()
