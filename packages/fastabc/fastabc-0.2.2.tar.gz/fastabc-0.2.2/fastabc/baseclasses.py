import typing as t
from fastapi import FastAPI, APIRouter
from .structures import FastAPIConfig

class App:
    def __init__(self, *args, lifespan: t.Optional[t.Callable] = None, **kwargs):
        if lifespan:
            kwargs["lifespan"] = lifespan
        self.app = FastAPI(*args, **kwargs)
        self.extensions = {}

    def loader(self, create_fn: t.Callable[[FastAPI], FastAPI], **kwargs):
        self.app = create_fn(self.app, **kwargs)
        return self.app

    def run_single(self, **kwargs):
        import uvicorn
        config = self.make_startup_config(**kwargs)
        uvicorn.run(self.app, host=config.host, port=config.port, debug=config.debug)

    def make_startup_config(self, **kwargs) -> FastAPIConfig:
        return FastAPIConfig.create({
            "host": kwargs.pop("host", "0.0.0.0"),
            "port": kwargs.pop("port", 8000),
            "debug": kwargs.pop("debug", False),
            **kwargs,
        })


class Api:
    def __init__(self, name: str, url_prefix: str = ""):
        self.router = APIRouter(prefix=url_prefix)
        self.name = name

    def new_routes(self, routes: t.Dict[str, t.Type]):
        for url, resource in routes.items():
            resource_instance = resource()
            for method_name in ["get", "post", "put", "delete"]:
                if hasattr(resource_instance, method_name):
                    method = getattr(resource_instance, method_name)
                    self.router.add_api_route(url, method, methods=[method_name.upper()])
        return self

    def init_app(self, app: FastAPI):
        app.include_router(self.router)
        return self
