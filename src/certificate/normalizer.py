# src/certificate/normalizer.py
"""
Нормализатор сертификата: переводит вещественные значения в интервалы
с небольшим запасом (upper >= value >= lower).
"""

from __future__ import annotations
from typing import Dict, Any
from copy import deepcopy

def normalize_certificate(raw: Dict[str, Any], margin: float = 1e-5) -> Dict[str, Any]:
    res = deepcopy(raw)

    if "delta_ph" in res:
        val = float(res["delta_ph"])
        lo = max(0.0, val - margin)
        hi = min(1.0, val + margin)
        res["delta_ph_interval"] = {"lower": lo, "upper": hi}
    else:
        res["delta_ph_interval"] = {"lower": 0.0, "upper": 1.0}

    # полусуррогатная метка времени/метаданные
    res.setdefault("meta", {})
    res["meta"].setdefault("normalized", True)

    return res
