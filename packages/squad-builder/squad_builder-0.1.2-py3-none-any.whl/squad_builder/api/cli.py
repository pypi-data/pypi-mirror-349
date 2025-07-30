import os
import yaml
import importlib
from fastapi import FastAPI
from .decorators import router, expose_api
import uvicorn

def discover_manifests(root_dir: str = "."):
    """Encontra todos os manifest.yaml a partir de root_dir."""
    manifests = []
    for dirpath, _, files in os.walk(root_dir):
        if "manifest.yaml" in files:
            full = os.path.join(dirpath, "manifest.yaml")
            data = yaml.safe_load(open(full, "r", encoding="utf-8"))
            data["_manifest_path"] = full
            data["_base_dir"] = dirpath
            manifests.append(data)
    return manifests

def register_teams(router, manifests):
    """Importa cada módulo/classe e aplica o decorator dinamicamente."""
    for m in manifests:
        module_path = m["team"]["module"]
        class_name  = m["team"]["class"]
        module = importlib.import_module(module_path)
        team_cls = getattr(module, class_name)
        expose_api(manifest_path=m["_manifest_path"])(team_cls)

def build_app():
    app = FastAPI(title="Squad Builder API")
    manifests = discover_manifests()
    register_teams(router, manifests)
    app.include_router(router)
    return app

# instância global que uvicorn irá expor
app = build_app()

def main():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("squad_builder.api.cli:app", host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    main()
