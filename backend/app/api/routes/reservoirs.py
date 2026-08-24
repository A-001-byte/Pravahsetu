"""Reservoir endpoints: currently a read-only listing of the three dams
(Koyna, Warna, Radhanagari). Forecast/advisory endpoints land here in
later modules.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.reservoir import list_reservoirs
from app.db.session import get_db
from app.schemas.reservoir import ReservoirOut

router = APIRouter(prefix="/reservoirs", tags=["reservoirs"])


@router.get("", response_model=list[ReservoirOut])
async def get_reservoirs(db: AsyncSession = Depends(get_db)) -> list[ReservoirOut]:
    return await list_reservoirs(db)
