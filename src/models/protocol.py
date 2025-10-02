# src/models/protocol.py
from typing import List, Dict, Any
from pydantic import BaseModel


class ComplexNumber(BaseModel):
    re: float
    im: float


class State(BaseModel):
    label: str
    p: float
    vec: List[ComplexNumber]


class POVMElement(BaseModel):
    label: str
    matrix: List[List[ComplexNumber]]


class Measurements(BaseModel):
    normalize: bool = True
    povm: List[POVMElement]


class Device(BaseModel):
    eta: float
    dark_count: float
    detector_efficiency: float


class ErrorCorrection(BaseModel):
    scheme: str
    target_ferr: float
    inefficiency_f: float


class PrivacyAmplification(BaseModel):
    method: str
    hash_family: str
    security_parameter: float


class Postprocessing(BaseModel):
    sifting: str
    error_correction: ErrorCorrection
    privacy_amplification: PrivacyAmplification


class Observed(BaseModel):
    p_conclusive: float
    error_rate_conclusive: float
    p_inconclusive: float


class SecurityGoal(BaseModel):
    output: str
    epsilon: float
    formula_hint: str


class MetaInfo(BaseModel):
    author: str
    email: str
    date: str
    notes: str


class ProtocolConfig(BaseModel):
    name: str
    description: str = ""
    parameters: Dict[str, Any]
    states: List[State]
    measurements: Measurements
    device: Device
    postprocessing: Postprocessing
    observed: Observed
    security_goal: SecurityGoal
    meta: MetaInfo
