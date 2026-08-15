import uuid
from collections import deque
from typing import Any, Dict

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.active_tasks = {}

    def add_task(self, task_type: str, params: Dict[str, Any]) -> str:
        task_id = str(uuid.uuid4())
        self.queue.append((task_id, task_type, params))
        return task_id

    def get_next(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def mark_complete(self, task_id: str):
        self.active_tasks.pop(task_id, None)
