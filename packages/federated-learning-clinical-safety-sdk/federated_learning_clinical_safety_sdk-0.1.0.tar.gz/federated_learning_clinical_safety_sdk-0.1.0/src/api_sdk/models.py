# src/my_api_sdk/models.py
from pydantic import BaseModel, Field

class FlModel(BaseModel):
    id: int | None = None
    name: str
    accuracy: float
    generalisability: float = Field(..., alias="generalisability")
    security: float | None = None

    class Config:
        allow_population_by_field_name = True

class LocalModel(BaseModel):
    id: int | None = None
    fl_model: int
    name: str
    relatability: float
    source: str
