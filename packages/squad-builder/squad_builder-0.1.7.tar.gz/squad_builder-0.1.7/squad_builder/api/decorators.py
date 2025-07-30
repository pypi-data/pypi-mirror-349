import inspect
from fastapi import APIRouter, Body
from typing import Type

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

        if len(params) == 1:  # apenas self
            @router.post(route)
            async def endpoint_func():
                team = team_cls(**manifest['team'].get('params', {}))
                return team.run()
        else:
            @router.post(route)
            async def endpoint_func(payload: dict = Body(...)):
                team = team_cls(**manifest['team'].get('params', {}))
                return team.run(payload)

        return team_cls

    return decorator
