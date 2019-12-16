# chat_server
python group chat server base on web socket.

single process
python chatserver.py 

mutiple process
gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -w 4 --bind 0:8000 chatserver

run max_client.py to test preformance

### Python异步性能和多进程
这个任务将考察你关于异步程序及其性能问题的能力。这个任务由两个子任务和一个聊天应用程序样例代码组成。

chatserver.py
index.html
requirements.txt

在安装了requirement.txt里的包后，运行以下命令，启动服务：

	python chatserver.py

你可以连接http: // localhost: 8000 来测试它。

### 多服务器传播实现(Multiserver Broadcast Implementation)
第一个子任务是修改已有的聊天应用，使得传播程序即便在多进程使用的情况依然完好运行。目前的聊天应用因为用了socket进行通信，并且信息存储在内存中，所以只能在单进程下运行。

一旦实现，我们希望使用以下命令来运行多进程：
	
	gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -w 4 -- bind 0: 8000 chatserver 

再连接http: //localhost:8000 来测试它。

我们建议后端使用rabbitmq或redis。如果相比gevent，你更熟悉其他如asyncio的异步技术，你可以创建一个新的chatserver.py。当然，你也需要写出你自己的gunicorn命令。在这种情形下，请告诉我们你用其他技术重新编写chatserver.py所花费的时间。

### 测试聊天服务的性能
编写一个测试客户端来测试你实现的聊天服务的性能。请使用Python，并且你可以使用任何你熟悉的异步技术。你需要测试的内容条件如下：

一个客户端每三秒发送一条信息
所有的客户端应该在一秒内收到任何信息

你可以编写代码去测试在上述条件下，最多可以有多少个客户端。请不要将网络问题或服务端与客户端的负载问题计算在内(Please do not count network problems, or server / client load sharing issues )。在你的个人电脑上应该可以同时运行服务端和客户端。
