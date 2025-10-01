from pathlib import Path
from ..models.protocol import ProtocolConfig

def generate_coq_code(config: ProtocolConfig) -> str:
    """Генерирует Coq код из конфигурации протокола"""
    # Пока возвращаем тестовый файл
    return "Theories/Core/Dummy.v"