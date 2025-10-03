# tests/test_cli_generate.py
import subprocess
from pathlib import Path
import sys

def test_cli_generate_creates_coq_file(tmp_path: Path):
    # Запускаем модуль как CLI (использует sys.executable окружения CI)
    result = subprocess.run(
        [sys.executable, "-m", "src.runner.generate_instance", "configs/instances/B92_protocol.toml"],
        check=False,
    )
    assert result.returncode == 0
    assert Path("coq/Generated/b92_inst.v").exists()
