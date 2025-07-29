from .baseclasses import App, Api

__version__ = "4.2.0"
__all__ = ["Api", "App"]


def start_server(create_fn, **config):
    app_instance = App()
    app = app_instance.loader(create_fn, **config)
    import uvicorn
    uvicorn.run(app, host=config.get("host", "0.0.0.0"), port=config.get("port", 8000))
