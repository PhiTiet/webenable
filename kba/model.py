from pydantic import BaseModel
from datetime import datetime
from enum import StrEnum

class Unit(StrEnum):
    kWh = "kWh"
    Wh = "Wh"

class Datapoint(BaseModel):
    timestamp: datetime
    value: float

class GraphData(BaseModel):
    goal: float
    slope: float
    history: list[Datapoint]
    unit: Unit

class DashboardResponse(BaseModel):
    daily_usage: GraphData
    daily_generation: GraphData
    monthly_total: GraphData
