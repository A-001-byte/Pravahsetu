"""Async SQLAlchemy engine/session setup, driven by DATABASE_URL.

Uses the `asyncpg` driver for the running app (async, per CLAUDE.md's
choice of FastAPI specifically for async, and this project's rule against
sync DB calls from async routes). psycopg2-binary stays in requirements
for Alembic, which runs synchronously.

TODO: wire up Alembic migrations against backend/db/schema.sql once the
schema stabilizes; for now schema.sql is applied directly via psql.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

# .env's DATABASE_URL uses the sync "postgresql://" scheme (shared with
# Alembic/psycopg2 later); swap in the asyncpg driver for the running app.
_ASYNC_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(_ASYNC_DATABASE_URL, echo=False, future=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding a request-scoped async DB session."""
    async with async_session_factory() as session:
        yield session
