import tomllib   # встроенный в Python 3.11+
# если используешь Python < 3.11, то ставь пакет: pip install tomli

from pathlib import Path
from ..models.protocol import ProtocolConfig


def load_protocol_config(config_path: str) -> ProtocolConfig:
    """Загружает конфигурацию протокола из TOML файла"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(path, "rb") as f:  # бинарный режим обязателен для tomllib
        data = tomllib.load(f)

    return ProtocolConfig(**data)
