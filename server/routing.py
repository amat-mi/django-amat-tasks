# coding: utf-8

channel_routing = {
#     "http.request": "server.consumers.http_consumer",
    "slow-channel": "server.consumers.slow_consumer",
    "task_result-channel": "server.consumers.task_result_consumer",
    "as_view": "server.consumers.as_view_consumer",
}
