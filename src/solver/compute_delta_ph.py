# src/solver/compute_delta_ph.py
"""
Заглушка решателя для оценки фазовой ошибки δ_ph.
В полном проекте здесь будет вызов SDP через CVXPY и извлечение дуального сертификата.
Сейчас возвращаем фиксированное значение и примитивный "сертификат".
"""

from __future__ import annotations
from typing import Dict, Any
from ..models.protocol import ProtocolConfig

def compute_delta_ph(config: ProtocolConfig) -> Dict[str, Any]:
    # Для MVP берём значение из observed, чтобы хоть как-то связать с входом
    # (например, δ_ph ≈ error_rate_conclusive + 0.03, с клиппингом в [0, 0.5])
    base = float(config.observed.error_rate_conclusive)
    delta_ph = min(max(base + 0.03, 0.0), 0.5)

    # Примитивный "сертификат" (в будущем: дуальные переменные SDP)
    dual_certificate = {
        "solver": "stub",
        "details": "no-duals-mvp",
        "note": "replace with CVXPY duals later",
    }

    return {
        "delta_ph": delta_ph,
        "certificate": dual_certificate,
    }
