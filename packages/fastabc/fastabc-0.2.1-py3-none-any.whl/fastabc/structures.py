from dataclasses import dataclass, replace, field


@dataclass
class FastAPIConfig:
    host: str = field(default="0.0.0.0")
    port: int = field(default=8000)
    debug: bool = field(default=False)
    access_log: bool = field(default=True)
    extra: dict = field(default_factory=dict)

    @classmethod
    def create(cls, config):
        result = cls(extra={k: v for k, v in config.items() if k not in {"host", "port", "debug", "access_log"}})
        if config.get("host"):
            result = replace(result, host=config["host"])
        if isinstance(config.get("port"), int) and config["port"] > 0:
            result = replace(result, port=config["port"])
        if isinstance(config.get("debug"), bool):
            result = replace(result, debug=config["debug"])
        if isinstance(config.get("access_log"), bool):
            result = replace(result, access_log=config["access_log"])
        return result

    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "debug": self.debug,
            "access_log": self.access_log,
            **self.extra
        }
