import yaml
from pathlib import Path
from ..models.protocol import ProtocolConfig

def load_protocol_config(config_path: str) -> ProtocolConfig:
    """Загружает конфигурацию протокола из YAML файла"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    return ProtocolConfig(**data)