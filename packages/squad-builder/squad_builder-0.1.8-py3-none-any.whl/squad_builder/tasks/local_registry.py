import threading
import uuid
from datetime import datetime
from typing import Callable, Any, Dict

_registry: Dict[str, dict] = {}

def create_task(func: Callable, *args, **kwargs) -> str:
    task_id = str(uuid.uuid4())
    _registry[task_id] = {
        "status": "pending",
        "started_at": datetime.utcnow().isoformat(),
        "result": None,
        "error": None,
        "ended_at": None,
    }

    def wrapper():
        _registry[task_id]["status"] = "running"
        try:
            result = func(*args, **kwargs)
            _registry[task_id]["result"] = result
            _registry[task_id]["status"] = "done"
        except Exception as e:
            _registry[task_id]["error"] = str(e)
            _registry[task_id]["status"] = "failed"
        finally:
            _registry[task_id]["ended_at"] = datetime.utcnow().isoformat()

    thread = threading.Thread(target=wrapper)
    thread.start()

    return task_id

def get_task(task_id: str) -> dict:
    return _registry.get(task_id)
