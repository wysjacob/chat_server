# chat_server
python group chat server base on web socket.

single process
python chatserver.py 

mutiple process
gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -w 4 --bind 0:8000 chatserver

run max_client.py to test preformance
