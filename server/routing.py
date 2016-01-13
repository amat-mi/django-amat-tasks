# coding: utf-8

channel_routing = {
#     "http.request": "server.consumers.http_consumer",
#     "slow-channel": "server.consumers.slow_consumer",
#     "task_result-channel": "server.consumers.task_result_consumer",

    "websocket.connect": "server.consumers.ws_add",
    "websocket.keepalive": "server.consumers.ws_add",
    "websocket.receive": "server.consumers.ws_message",
    "websocket.disconnect": "server.consumers.ws_disconnect",
}
