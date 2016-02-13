# coding: utf-8

channel_routing = {
#     "http.request": "server.consumers.http_consumer",
    "slow-channel": "server.consumers.slow_consumer",
    "as_view": "server.consumers.as_view_consumer",

    "task_result-channel": "tasks.consumers.task_result_consumer",
    "taskrun-channel": "tasks.consumers.taskrun_consumer",

    "task-run": "tasks.models.task_run_consumer",
    "task-progress": "tasks.models.task_progress_consumer",    
}
