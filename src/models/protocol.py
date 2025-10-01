# src/__init__.py - сделать пакетом
# src/models/protocol.py - базовые модели данных
from pydantic import BaseModel
from typing import Dict, Any

class ProtocolConfig(BaseModel):
    name: str
    parameters: Dict[str, Any]
    
