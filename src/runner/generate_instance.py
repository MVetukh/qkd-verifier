# src/runner/generate_instance.py
"""
Единая точка запуска для MVP-пайплайна:
- чтение конфигурации;
- вычисление δ_ph (заглушка);
- нормализация сертификата;
- генерация Coq-файла coq/Generated/b92_inst.v;
- сохранение certificate.json (для будущей отладки/просмотра).
"""

from __future__ import annotations
import json
from pathlib import Path

from ..parser.toml_parser import load_protocol_config as load_toml
try:
    from ..parser.yaml_parser import load_yaml_config as load_yaml
except Exception:
    load_yaml = None  # если PyYAML не стоит

from ..solver.compute_delta_ph import compute_delta_ph
from ..certificate.normalizer import normalize_certificate
from ..generator.coq_generator import generate_coq_file

def main_cli():
    """
    Консольная точка входа (pyproject [project.scripts]).
    По умолчанию использует configs/instances/B92_protocol.toml,
    но можно передать путь через переменную окружения QKD_CONFIG
    или аргумент командной строки.
    """
    import os, sys
    cfg = None
    if len(sys.argv) > 1:
        cfg = sys.argv[1]
    else:
        cfg = os.environ.get("QKD_CONFIG", "configs/instances/B92_protocol.toml")
    main(cfg)

def main(config_path: str) -> None:
    p = Path(config_path)
    if not p.exists():
        raise FileNotFoundError(p)

    if p.suffix.lower() in (".toml",):
        cfg = load_toml(p)
    elif p.suffix.lower() in (".yaml", ".yml") and load_yaml:
        cfg = load_yaml(p)
    else:
        raise ValueError("Unsupported config extension or YAML parser missing.")

    raw = compute_delta_ph(cfg)
    cert = normalize_certificate(raw)

    # сохранить сертификат для отладки
    out_cert = Path("coq") / "Generated" / "certificate.json"
    out_cert.parent.mkdir(parents=True, exist_ok=True)
    out_cert.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    out_v = generate_coq_file(cfg, cert)
    print(f"OK: wrote {out_cert} and {out_v}")

if __name__ == "__main__":
    # по умолчанию гоняем на примере B92_protocol.toml
    main("configs/instances/B92_protocol.toml")
