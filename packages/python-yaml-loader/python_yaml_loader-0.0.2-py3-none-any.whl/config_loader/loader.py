import yaml
from pathlib import Path
from copy import deepcopy

class YamlConfigLoader:
    def __init__(self, config_file=None, profile=None):
        self.config_file = Path(config_file or "application.yml")
        self.profile = profile
        self._config = self._load()

    def _load(self):
        if not self.config_file.exists():
            print(
                f"[YamlConfigLoader] ⚠️ Config file not found:"
                f" {self.config_file} (using empty config)"
            )
            return {}

        with open(self.config_file) as f:
            base_data = yaml.safe_load(f) or {}

        # === 1. Profile keresése 'profiles' kulcs alatt ===
        if self.profile and 'profiles' in base_data:
            profile_data = base_data['profiles'].get(self.profile, {})
            return self._deep_merge(base_data, profile_data)

        # === 2. Profile root szinten ===
        if self.profile and self.profile in base_data:
            default_data = base_data.get("default", {})
            profile_data = base_data.get(self.profile, {})
            return self._deep_merge(default_data, profile_data)

        # === 3. Profile külön fájlban ===
        if self.profile:
            profile_file = self._get_profile_filename(self.config_file)
            if profile_file.exists():
                with open(profile_file) as pf:
                    profile_data = yaml.safe_load(pf) or {}
                    return self._deep_merge(base_data, profile_data)

        return base_data

    def _get_profile_filename(self, base_path: Path) -> Path:
        stem = base_path.stem.split(".")[0]
        return base_path.with_name(f"{stem}-{self.profile}.yml")

    def _deep_merge(self, base: dict, override: dict) -> dict:
        result = deepcopy(base)
        for k, v in override.items():
            if (
                k in result and isinstance(result[k], dict)
                and isinstance(v, dict)
            ):
                result[k] = self._deep_merge(result[k], v)
            else:
                result[k] = deepcopy(v)
        return result

    def get(self, key, default=None):
        keys = key.split(".")
        value = self._config
        for k in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(k)
            if value is None:
                return default
        return value
