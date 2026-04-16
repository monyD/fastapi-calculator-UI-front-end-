import json
from importlib import import_module


def list_routes(modname):
    try:
        mod = import_module(modname)
        app = getattr(mod, "app", None)
        if app is None:
            return {"module": modname, "error": "no app attribute found"}
        routes = [r.path for r in app.routes]
        return {"module": modname, "routes": routes}
    except Exception as e:
        return {"module": modname, "error": str(e)}


if __name__ == "__main__":
    print(json.dumps(list_routes("app.main_ui"), indent=2))