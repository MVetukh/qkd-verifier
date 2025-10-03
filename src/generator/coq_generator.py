# src/generator/coq_generator.py
"""
Генерация Coq-файла по шаблону Jinja2.
Берём ProtocolConfig + нормализованный сертификат и создаём coq/Generated/b92_inst.v
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ..models.protocol import ProtocolConfig

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE / "templates"
GEN_OUT = Path("coq") / "Generated" / "b92_inst.v"

def _coq_real(x: float) -> str:
    # представление вещественных чисел в Coq (как R-константы)
    return f"({x:.10f})%R"

def generate_coq_file(config: ProtocolConfig, cert: Dict[str, Any], out_path: Path = GEN_OUT) -> Path:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=False,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["coq_real"] = _coq_real

    tpl = env.get_template("instance.v.j2")

    params = config.parameters
    p0 = float(params.get("p_psi0", 0.5))
    p1 = float(params.get("p_psi1", 0.5))
    N = int(params.get("N", 1000))

    dph_lo = float(cert["delta_ph_interval"]["lower"])
    dph_hi = float(cert["delta_ph_interval"]["upper"])

    rendered = tpl.render(
        N=N, p_psi0=p0, p_psi1=p1,
        delta_ph_lower=dph_lo,
        delta_ph_upper=dph_hi,
        epsilon=float(config.security_goal.epsilon),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    return out_path
