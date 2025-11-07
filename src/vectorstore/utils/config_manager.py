from source.backend.utils.config_loader import ConfigLoader
from box import Box
import os

class Config:
    _instance = None

    def __new__(cls, config_file: str = None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config(config_file)
        return cls._instance

    def _load_config(self, config_file: str = None):
        config_file = config_file or os.getenv("CONFIG_FILE", "configs/config.yaml")
        merged_config = ConfigLoader.load_config(config_file)
        self._config = Box(merged_config, default_box=True)

    @property
    def cfg(self):
        return self._config

    def reload(self, config_file: str = None):
        self._load_config(config_file)