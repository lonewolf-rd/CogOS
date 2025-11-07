import yaml
import os


class ConfigLoader:
    CONFIG_DIR = os.path.join(os.path.dirname(__file__), "../configs")

    @staticmethod
    def load_yaml(file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r") as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def merge_configs(base: dict, override: dict) -> dict:
        merged = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = ConfigLoader.merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged

    @staticmethod
    def load_config(config_file: str) -> dict:
        if not config_file.endswith(".yaml"):
            config_file += ".yaml"

        config_path = os.path.join(ConfigLoader.CONFIG_DIR, config_file)

        template_path = config_path.replace(".yaml", "_template.yaml")
        template_config = ConfigLoader.load_yaml(template_path)

        actual_config = ConfigLoader.load_yaml(config_path)

        merged_config = ConfigLoader.merge_configs(template_config, actual_config)

        includes = merged_config.pop("include", [])
        for inc_file in includes:
            inc_path = os.path.join(ConfigLoader.CONFIG_DIR, inc_file)
            inc_data = ConfigLoader.load_yaml(inc_path)
            merged_config = ConfigLoader.merge_configs(merged_config, inc_data)

        return merged_config