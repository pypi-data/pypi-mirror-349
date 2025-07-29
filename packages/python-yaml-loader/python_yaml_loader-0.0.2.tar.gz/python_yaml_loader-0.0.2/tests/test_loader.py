import pytest
from config_loader.loader import YamlConfigLoader
from pathlib import Path

BASE = Path(__file__).parent / "resources"

def test_basic_loading():
    loader = YamlConfigLoader(BASE / "base.yml")
    assert loader.get("app.name") == "test-app"
    assert loader.get("app.debug") is False

def test_nested_key_access():
    loader = YamlConfigLoader(BASE / "with_profiles.yml", profile="dev")
    assert loader.get("database.connection.host") == "localhost"
    assert loader.get("database.connection.port") == 5432

def test_profile_override():
    loader = YamlConfigLoader(BASE / "with_profiles.yml", profile="prod")
    assert loader.get("app.debug") is False
    assert loader.get("database.connection.host") == "prod.db.internal"

def test_missing_key_returns_default():
    loader = YamlConfigLoader(BASE / "base.yml")
    assert loader.get("nonexistent.key", default="fallback") == "fallback"

def test_missing_file_returns_empty_config(capfd):
    loader = YamlConfigLoader(config_file="nonexistent.yml")
    assert loader.get("anything") is None

    out, err = capfd.readouterr()
    assert "Config file not found" in out

def test_invalid_yaml_raises():
    with pytest.raises(Exception):
        YamlConfigLoader(BASE / "invalid.yml")

def test_profile_root_level_override():
    loader = YamlConfigLoader(BASE / "root_profiles.yml", profile="prod")
    assert loader.get("app.name") == "my-prod-app"
    assert loader.get("app.debug") is False
    assert loader.get("feature.enabled") is True

def test_profile_separate_file():
    loader = YamlConfigLoader(BASE / "multi_file_base.yml", profile="test")
    assert loader.get("service.name") == "test-service"
    assert loader.get("service.debug") is True

def test_deep_merge_override_nested_values():
    loader = YamlConfigLoader(BASE / "merge_base.yml", profile="custom")
    assert loader.get("nested.level1.level2") == "override"
    assert loader.get("nested.level1.keep") == "original"

def test_deep_merge_non_dict_override():
    loader = YamlConfigLoader(BASE / "merge_base.yml", profile="scalar_override")
    assert loader.get("scalar") == "replaced"

def test_unknown_profile_falls_back_to_base():
    loader = YamlConfigLoader(BASE / "base.yml", profile="nonexistent")
    assert loader.get("app.name") == "test-app"
    assert loader.get("app.debug") is False

def test_get_fails_on_non_dict_intermediate():
    loader = YamlConfigLoader(BASE / "base.yml")
    # app.name == "test-app", tehát string -> nem tudunk továbblépni mélyebbre
    assert loader.get("app.name.subkey", default="fail-safe") == "fail-safe"
