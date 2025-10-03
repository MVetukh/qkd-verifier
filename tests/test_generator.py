# tests/test_generator.py
import json
from pathlib import Path

from src.parser.toml_parser import load_protocol_config
from src.solver.compute_delta_ph import compute_delta_ph
from src.certificate.normalizer import normalize_certificate
from src.generator.coq_generator import generate_coq_file

def test_generate_b92_coq(tmp_path: Path):
    # используем реальный конфиг из репозитория
    cfg_path = Path("configs/instances/B92_protocol.toml")
    assert cfg_path.exists(), "B92_protocol.toml not found"

    cfg = load_protocol_config(cfg_path)

    # шаги пайплайна
    raw = compute_delta_ph(cfg)
    cert = normalize_certificate(raw, margin=1e-5)

    # сохраним сертификат рядом с артефактами (временная папка для теста)
    out_dir = tmp_path / "coq" / "Generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "certificate.json").write_text(json.dumps(cert, indent=2), encoding="utf-8")

    # сгенерируем Coq файл именно в tmp, чтобы не трогать репозиторий
    out_v = out_dir / "b92_inst.v"
    path = generate_coq_file(cfg, cert, out_path=out_v)

    assert path.exists(), "Generated b92_inst.v not created"

    content = path.read_text(encoding="utf-8")
    # Пара простых сигнатур для sanity-check
    assert "Definition delta_ph_lower" in content
    assert "Definition delta_ph_upper" in content
    assert "Theorem b92_security_stub" in content
