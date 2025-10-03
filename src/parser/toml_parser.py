# src/parser/toml_parser.py
"""
Парсинг TOML-конфигурации протокола в структуру ProtocolConfig.
Работает на Python 3.8+:
- 3.11+: используется stdlib tomllib
- <3.11: используется пакет tomli (если установлен)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # Python < 3.11 (линтер может ворчать — это ок)
    import tomli as tomllib  # type: ignore[no-redef]

from ..models.protocol import (
    ProtocolConfig,
    ComplexNumber,
    State,
    POVMElement,
    Measurements,
    Device,
    ErrorCorrection,
    PrivacyAmplification,
    Postprocessing,
    Observed,
    SecurityGoal,
    MetaInfo,
)


def _cn(d: Dict[str, Any]) -> ComplexNumber:
    return ComplexNumber(re=float(d["re"]), im=float(d["im"]))


def _matrix(m: List[List[Dict[str, Any]]]) -> List[List[ComplexNumber]]:
    return [[_cn(c) for c in row] for row in m]


def load_protocol_config(config_path: str | Path) -> ProtocolConfig:
    """Загружает конфигурацию протокола из TOML файла и маппит в ProtocolConfig."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, "rb") as f:  # бинарный режим обязателен для tomllib/tomli
        data: Dict[str, Any] = tomllib.load(f)

    # ---- name/description: в TOML они лежат в [protocol], в модели — на верхнем уровне
    if "protocol" in data:
        name = str(data["protocol"].get("name", ""))
        description = str(data["protocol"].get("description", ""))
    else:
        # резерв: поддержка альтернативной YAML-формы с верхним name
        name = str(data.get("name", ""))
        description = str(data.get("description", ""))

    # ---- states
    states = [
        State(
            label=s["label"],
            p=float(s["p"]),
            vec=[_cn(c) for c in s["vec"]],
        )
        for s in data.get("states", [])
    ]

    # ---- measurements / POVM
    meas = data.get("measurements", {})
    povm = [
        POVMElement(
            label=pe["label"],
            matrix=_matrix(pe["matrix"]),
        )
        for pe in meas.get("povm", [])
    ]
    measurements = Measurements(
        normalize=bool(meas.get("normalize", True)),
        povm=povm,
    )

    # ---- device
    dev = data.get("device", {})
    device = Device(
        eta=float(dev["eta"]),
        dark_count=float(dev["dark_count"]),
        detector_efficiency=float(dev["detector_efficiency"]),
    )

    # ---- postprocessing
    pp = data.get("postprocessing", {})
    ec = pp.get("error_correction", {})  # для TOML: это секция [postprocessing.error_correction]
    # если у тебя было YAML-подобное двоеточие — уже исправил на секцию [postprocessing.error_correction]
    error_correction = ErrorCorrection(
        scheme=str(ec["scheme"]),
        target_ferr=float(ec["target_ferr"]),
        inefficiency_f=float(ec["inefficiency_f"]),
    )

    pa = pp.get("privacy_amplification", {})  # [postprocessing.privacy_amplification]
    privacy_amplification = PrivacyAmplification(
        method=str(pa["method"]),
        hash_family=str(pa["hash_family"]),
        security_parameter=float(pa["security_parameter"]),
    )

    postprocessing = Postprocessing(
        sifting=str(pp["sifting"]),
        error_correction=error_correction,
        privacy_amplification=privacy_amplification,
    )

    # ---- observed
    obs = data.get("observed", {})
    observed = Observed(
        p_conclusive=float(obs["p_conclusive"]),
        error_rate_conclusive=float(obs["error_rate_conclusive"]),
        p_inconclusive=float(obs["p_inconclusive"]),
    )

    # ---- security_goal
    sg = data.get("security_goal", {})
    security_goal = SecurityGoal(
        output=str(sg["output"]),
        epsilon=float(sg["epsilon"]),
        formula_hint=str(sg["formula_hint"]),
    )

    # ---- meta
    meta_in = data.get("meta", {})
    meta = MetaInfo(
        author=str(meta_in["author"]),
        email=str(meta_in["email"]),
        date=str(meta_in["date"]),
        notes=str(meta_in["notes"]),
    )

    # ---- parameters: в модели — произвольный словарь
    parameters = data.get("parameters", {})

    return ProtocolConfig(
        name=name,
        description=description,
        parameters=parameters,
        states=states,
        measurements=measurements,
        device=device,
        postprocessing=postprocessing,
        observed=observed,
        security_goal=security_goal,
        meta=meta,
    )


if __name__ == "__main__":
    cfg = load_protocol_config("configs/instances/B92_protocol.toml")
    print(cfg)
