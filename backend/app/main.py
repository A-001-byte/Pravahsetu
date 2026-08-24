"""FastAPI application entrypoint.

Advisory only: this service exposes recommendations, it does not expose
any gate-control action.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.reservoirs import router as reservoirs_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Pravaha Setu",
        description=(
            "Advisory-only coordinated flood-release API for the Koyna, Warna, "
            "and Radhanagari reservoirs (Kolhapur, Upper Krishna Basin)."
        ),
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(reservoirs_router)

    return app


app = create_app()
