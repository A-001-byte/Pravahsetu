"""SQLAlchemy ORM models mirroring backend/db/schema.sql.

Tables: reservoirs, reservoir_observations, rainfall_grid,
gauge_observations, forecast_runs, advisory_runs. See CLAUDE.md > Module
breakdown and Resources Required > Datasets for what each field maps to.

Deviation from the team's schema doc: `reservoirs.lat`/`lon` are plain
FLOAT columns here, not a PostGIS GEOGRAPHY(POINT). We don't have any
spatial-query work in v1 scope (no river-network geometry), so adding
GeoAlchemy2 now would be dependency weight with no use yet. Swap back to
GEOGRAPHY(POINT) + GeoAlchemy2 if/when that changes (see CLAUDE.md > Tech
stack, PostGIS is listed as optional).
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Reservoir(Base):
    """One of the three reservoirs in scope: Koyna, Warna, Radhanagari."""

    __tablename__ = "reservoirs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    lat: Mapped[float | None] = mapped_column(Float)
    lon: Mapped[float | None] = mapped_column(Float)
    max_storage_mcm: Mapped[float | None] = mapped_column(Float)
    catchment_area_sqkm: Mapped[float | None] = mapped_column(Float)

    observations: Mapped[list[ReservoirObservation]] = relationship(back_populates="reservoir")


class ReservoirObservation(Base):
    """Daily inflow/outflow/storage record for one reservoir (Module 1)."""

    __tablename__ = "reservoir_observations"
    __table_args__ = (
        UniqueConstraint(
            "reservoir_id",
            "obs_date",
            "source",
            name="uq_reservoir_observations_reservoir_date_source",
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reservoir_id: Mapped[int] = mapped_column(ForeignKey("reservoirs.id"), nullable=False)
    obs_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    storage_mcm: Mapped[float | None] = mapped_column(Float)
    inflow_cumecs: Mapped[float | None] = mapped_column(Float)
    outflow_cumecs: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String, nullable=False)

    reservoir: Mapped[Reservoir] = relationship(back_populates="observations")


class RainfallGrid(Base):
    """Catchment rainfall record for one reservoir (Module 1).

    Named `rainfall_grid` to match the team's schema doc, even though
    rows here are per-catchment scalars rather than a literal grid.
    """

    __tablename__ = "rainfall_grid"
    __table_args__ = (
        UniqueConstraint(
            "reservoir_id", "obs_date", "source", name="uq_rainfall_grid_reservoir_date_source"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reservoir_id: Mapped[int] = mapped_column(ForeignKey("reservoirs.id"), nullable=False)
    obs_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    rainfall_mm: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String, nullable=False)


class GaugeObservation(Base):
    """Downstream river gauge record, e.g. Rajaram Weir, Sangli (Module 1)."""

    __tablename__ = "gauge_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gauge_name: Mapped[str] = mapped_column(String, nullable=False)
    obs_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    obs_time: Mapped[dt.time | None] = mapped_column(Time)
    stage_m: Mapped[float | None] = mapped_column(Float)
    discharge_cumecs: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str | None] = mapped_column(String)


class ForecastRun(Base):
    """One inflow-forecast run for one reservoir (Module 3)."""

    __tablename__ = "forecast_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reservoir_id: Mapped[int] = mapped_column(ForeignKey("reservoirs.id"), nullable=False)
    run_timestamp: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)
    forecast_horizon_hrs: Mapped[int | None] = mapped_column(Integer)
    predicted_inflow_cumecs: Mapped[list[float] | None] = mapped_column(ARRAY(Float))
    model_version: Mapped[str | None] = mapped_column(String)


class AdvisoryRun(Base):
    """One coordinated-release recommendation, staggered vs. baseline (Module 4)."""

    __tablename__ = "advisory_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_timestamp: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)
    recommended_schedule: Mapped[dict | None] = mapped_column(JSONB)
    baseline_schedule: Mapped[dict | None] = mapped_column(JSONB)
    projected_peak_kolhapur: Mapped[float | None] = mapped_column(Float)
    projected_peak_sangli: Mapped[float | None] = mapped_column(Float)
