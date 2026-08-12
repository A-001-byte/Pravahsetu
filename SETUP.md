# Setup

Instructions to get a working development environment for Pravaha Setu.
This currently covers the Python side only (data pipeline, routing,
forecasting, advisor, simulation). Backend and frontend setup will be added
once those modules are scaffolded (Module 6).

## Prerequisites

- Python 3.11+
- Git
- PostgreSQL 14+ — only needed once the backend (Module 6) exists
- Node.js 18+ — only needed once the frontend (Module 6) exists

## 1. Clone and enter the repo

```bash
git clone https://github.com/A-001-byte/Pravahsetu.git
cd Pravahsetu
```

## 2. Python environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements-dev.txt
pip install -e .          # installs src/pravaha_setu in editable mode
```

## 3. Environment variables

```bash
cp .env.example .env
```

Then fill in real values (database credentials, API keys, etc.) in `.env`.
Never commit `.env`.

## 4. Pre-commit hooks (black + ruff)

```bash
pre-commit install
```

## 5. Run tests

```bash
pytest
```

## 6. Data

Raw source data is **not** committed to the repo (see `.gitignore`). Place
raw exports under:

```
data/raw/koyna/
data/raw/warna/
data/raw/radhanagari/
data/raw/gauges/
data/raw/rainfall/
```

Event-specific extracts used for routing calibration and backtesting go
under `data/events/2019/` and `data/events/2021/`.

Expected sources: India-WRIS, Central Water Commission, Maharashtra Water
Resources Department, India Meteorological Department, and published
official flood-investigation reports. See CLAUDE.md > Resources Required >
Datasets for the full list.

## 7. Backend / frontend (Module 6 — not yet built)

`docker-compose` usage and frontend `npm install` instructions will be added
here once the backend and frontend are scaffolded.

## Current status

Only the repository skeleton exists right now — see [README.md](README.md)
and [CLAUDE.md](CLAUDE.md) for the module build order. No module logic is
implemented yet.
