"""Persistence helpers for the Reservoir model."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Reservoir


async def list_reservoirs(db: AsyncSession) -> list[Reservoir]:
    result = await db.execute(select(Reservoir).order_by(Reservoir.name))
    return list(result.scalars().all())
