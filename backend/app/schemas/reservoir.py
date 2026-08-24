"""Pydantic response schemas for reservoir endpoints."""

from pydantic import BaseModel, ConfigDict


class ReservoirOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lat: float | None = None
    lon: float | None = None
    max_storage_mcm: float | None = None
    catchment_area_sqkm: float | None = None
