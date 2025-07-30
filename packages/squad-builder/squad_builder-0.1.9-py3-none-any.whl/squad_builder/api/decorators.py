import inspect
from fastapi import APIRouter, Body
from typing import Type
from squad_builder.tasks.local_registry import create_task, get_task

router = APIRouter()

def load_manifest(path: str) -> dict:
    import yaml
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def expose_api(manifest_path: str, endpoint: str = None):
    manifest = load_manifest(manifest_path)
    team_name = manifest['team']['name']
    route = endpoint or f"/{team_name}"

    def decorator(team_cls: Type):
        sig = inspect.signature(team_cls.run)
        params = list(sig.parameters.values())

        # Define POST /<team>
        if len(params) == 1:  # apenas self
            @router.post(route)
            async def async_run():
                team = team_cls(**manifest['team'].get('params', {}))
                task_id = create_task(team.run)
                return {"task_id": task_id}

        else:
            @router.post(route)
            async def async_run(payload: dict = Body(...)):
                team = team_cls(**manifest['team'].get('params', {}))
                task_id = create_task(team.run, payload)
                return {"task_id": task_id}

        # Define GET /<team>/{task_id}
        @router.get(f"{route}/{{task_id}}")
        async def get_status(task_id: str):
            task = get_task(task_id)
            if not task:
                return {"error": "task_id not found"}, 404
            return task

        return team_cls


    return decorator
