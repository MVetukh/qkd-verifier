# src/parser/yaml_parser.py
"""
Парсинг YAML-конфигурации протокола в структуру ProtocolConfig.
Зависимость: pyyaml (PyYAML).
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List

import yaml

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

def load_yaml_config(path: str | Path) -> ProtocolConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"YAML config not found: {p}")

    data = yaml.safe_load(p.read_text(encoding="utf-8"))

    states = [
        State(
            label=s["label"],
            p=float(s["p"]),
            vec=[_cn(c) for c in s["vec"]],
        )
        for s in data.get("states", [])
    ]

    povm = [
        POVMElement(
            label=pe["label"],
            matrix=_matrix(pe["matrix"]),
        )
        for pe in data.get("measurements", {}).get("povm", [])
    ]

    measurements = Measurements(
        normalize=bool(data.get("measurements", {}).get("normalize", True)),
        povm=povm,
    )

    device = Device(
        eta=float(data["device"]["eta"]),
        dark_count=float(data["device"]["dark_count"]),
        detector_efficiency=float(data["device"]["detector_efficiency"]),
    )

    ec = data["postprocessing"]["error_correction"]
    error_correction = ErrorCorrection(
        scheme=str(ec["scheme"]),
        target_ferr=float(ec["target_ferr"]),
        inefficiency_f=float(ec["inefficiency_f"]),
    )

    pa = data["postprocessing"]["privacy_amplification"]
    privacy_amplification = PrivacyAmplification(
        method=str(pa["method"]),
        hash_family=str(pa["hash_family"]),
        security_parameter=float(pa["security_parameter"]),
    )

    postprocessing = Postprocessing(
        sifting=str(data["postprocessing"]["sifting"]),
        error_correction=error_correction,
        privacy_amplification=privacy_amplification,
    )

    observed = Observed(
        p_conclusive=float(data["observed"]["p_conclusive"]),
        error_rate_conclusive=float(data["observed"]["error_rate_conclusive"]),
        p_inconclusive=float(data["observed"]["p_inconclusive"]),
    )

    security_goal = SecurityGoal(
        output=str(data["security_goal"]["output"]),
        epsilon=float(data["security_goal"]["epsilon"]),
        formula_hint=str(data["security_goal"]["formula_hint"]),
    )

    meta = MetaInfo(
        author=str(data["meta"]["author"]),
        email=str(data["meta"]["email"]),
        date=str(data["meta"]["date"]),
        notes=str(data["meta"]["notes"]),
    )

    return ProtocolConfig(
        name=str(data["protocol"]["name"]) if "protocol" in data else str(data["name"]),
        description=str(data.get("protocol", {}).get("description", "")),
        parameters=data["parameters"],
        states=states,
        measurements=measurements,
        device=device,
        postprocessing=postprocessing,
        observed=observed,
        security_goal=security_goal,
        meta=meta,
    )
