from pydantic import BaseModel
from typing import Dict, List

class MetricRangeRequest(BaseModel):
    name: List[str]
    labels: Dict
    start: int
    end: int
    step: int

class Metric(BaseModel):
    metric: Dict
    values: List[List[float]]

class MetricResponse(BaseModel):
    status: str
    data: List[Metric]