import yaml
import inspect
from fastapi import APIRouter, Body
from typing import Type

router = APIRouter()

def load_manifest(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def expose_api(manifest_path: str, endpoint: str = None):
    """
    Decorator que registra um endpoint POST para a classe do team.
    - manifest_path: caminho para o manifest.yaml
    - endpoint: rota opcional; por padrão usa team.name
    """
    manifest = load_manifest(manifest_path)
    team_name = manifest['team']['name']
    route = endpoint or f"/{team_name}"

    def decorator(team_cls: Type):
        # supõe que a classe tem método run(payload: dict) -> dict
        @router.post(route)
        async def _(payload: dict = Body(...)):
            team = team_cls(**manifest.get('team').get('params', {}))
            return team.run(payload)
        return team_cls
    return decorator
