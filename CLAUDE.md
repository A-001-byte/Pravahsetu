# Pravaha Setu — Project Context for Claude Code

This file is auto-loaded by Claude Code at the start of every session in this repo.
It exists so any team member (or Claude) starting fresh has the full picture without
re-explaining the project from scratch.

## What this project is

**Pravaha Setu** — A system for coordinating flood releases from multiple reservoirs,
for the Kolhapur and Sangli region, Upper Krishna Basin, Maharashtra.

Semester project for Vishwakarma Institute of Technology, Department of Computer
Engineering. Faculty coordinator: Dr. Manisha Mali. Submitted as a formal proposal
to the college's ERI channel for onward submission to a central government team;
approved to begin build.

## The problem

Kolhapur and Sangli flood badly and repeatedly (worst in 2019 and 2021). A major
contributing factor: upstream dams (Koyna, Warna, Radhanagari — each run by a
different division; a fourth, Almatti, is in Karnataka under a different state)
release water with no shared plan, coordinating only via emergency phone calls.
Because each dam is a different distance from the two cities, water from
simultaneous releases can arrive downstream at nearly the same time and stack
into a much bigger flood peak than any one dam would cause alone.

## What we're building

A system that:
1. Forecasts short-term inflow into each of the three reservoirs from rainfall data.
2. Calculates flood-wave travel time from each dam to Kolhapur/Sangli using
   hydrological routing (Muskingum method).
3. Uses the travel-time differences to recommend a **staggered** release schedule
   (and pre-emptive drawdown ahead of a forecast peak) so peaks don't stack downstream.
4. Presents this as a dashboard: "here's what we recommend, here's what happens if
   releases aren't coordinated."

**Critical constraint: advisory only.** The system never controls gates. It only
recommends. Every release decision stays with human operators and authorities.

## Scope (v1 — do not expand without discussion)

- **Three dams only**: Koyna, Warna, Radhanagari feeding Kolhapur. Almatti/Karnataka
  and full Sangli-basin coordination are explicitly future work — do not build for
  them now.
- **Hydrological routing, not full hydraulics**: Muskingum method or a calibrated
  fixed-lag model. No 2D hydrodynamic simulation (e.g. HEC-RAS) in v1.
- **Rule-based / constrained-optimization advisory logic in v1**, not reinforcement
  learning. RL is explicitly future work.
- **Report results as reduction in the dam-attributable portion of the flood peak**,
  never as "flood prevention." A large share of the flood comes from local/tributary
  rainfall (e.g. into the Panchganga) that no dam coordination can affect. Don't
  overclaim in any generated docs, README, or dashboard copy.
- Validation target: back-test recommendations against the real 2019 and 2021 floods.

## Team

| Name | Role/module (assign as needed) | Email |
|---|---|---|
| Aditi Thorat | | aditi.thorat24@vit.edu |
| Saachi Shalgar | | saachi.shalgar24@vit.edu |
| Kunal Yawatkar | | kunal.yawatkar24@vit.edu |
| Ankit Vyavahare | | ankit.vyavahare24@vit.edu |

## Module breakdown (build in roughly this order)

1. **Data pipeline** — ingest/clean historical inflow, outflow, reservoir-level,
   downstream gauge, and rainfall data; build the 2019/2021 event datasets used
   for validation.
2. **Flood routing / travel-time engine** — Muskingum routing calibrated against
   observed 2019/2021 hydrographs. Build this early; it's simpler and more
   isolated than the forecasting model, and everything downstream depends on it.
3. **Inflow forecasting engine** — start with a scikit-learn baseline (Random
   Forest / Gradient Boosting) before building the LSTM. Keep the baseline as a
   permanent comparison point, not a throwaway.
4. **Coordinated release advisor** — combines routing + forecasts into staggered
   release recommendations, including pre-emptive drawdown logic.
5. **Scenario simulation & backtesting** — reconstruct downstream hydrograph under
   "coordinated" vs "uncoordinated" scenarios; back-test against 2019/2021.
6. **Dashboard, API, deployment** — operator-facing UI, backend API, Docker,
   hosting.

## Tech stack

**Data / ML (Python 3.11+)**
- Pandas, NumPy for cleaning/merging time series
- Parquet for storage once data volume grows (not CSV)
- Pandera or Great Expectations (optional) for data validation
- scikit-learn for baseline forecasting models
- PyTorch for the LSTM inflow forecaster
- Optuna for hyperparameter tuning
- Consider NeuralHydrology (existing open-source LSTM rainfall-runoff library)
  before building the LSTM pipeline from scratch
- SciPy.optimize for calibrating Muskingum routing parameters
- PuLP or scipy.optimize.linprog if framing release staggering as constrained
  optimization rather than pure rule logic
- pytest for regression tests — especially on routing/advisory logic, where a
  silent bug is worse than in the UI
- Jupyter for exploratory backtesting only; port final logic into `.py` modules,
  don't leave the pipeline living in notebooks

**Backend**
- FastAPI (not Flask) — async, auto OpenAPI docs, Pydantic validation built in
- Pydantic for request/response schemas
- Uvicorn as ASGI server
- Default to a single FastAPI backend serving API + frontend build unless the
  team specifically wants a separate Node/Express layer

**Database**
- PostgreSQL (not MongoDB — this data is relational/time-series)
- TimescaleDB extension if time-series volume grows large
- PostGIS extension for river network geometry and dam locations
- SQLAlchemy ORM + Alembic for migrations

**Frontend**
- React + Vite + TypeScript
- Tailwind CSS + shadcn/ui
- Recharts (simpler) or Plotly.js (better interactivity) for hydrograph charts
- Leaflet for the basin/river map (preferred over Cesium.js — 2D is faster to
  build and the 3D globe adds visual flash without technical substance for this
  project)
- Zustand or plain React state — no Redux needed at this scale

**Packaging / deployment**
- Docker + docker-compose (Postgres + backend + frontend in one file, so anyone
  can spin up the whole system with one command)
- Vercel (frontend) + Render (backend + Postgres) — free tiers sufficient for demo
- GitHub Actions running pytest on every push

**Team hygiene**
- One shared GitHub repo, branch-per-module, PRs to merge
- pre-commit with black (formatting) + ruff (linting)
- Shared `.env.example` and a `SETUP.md` so the demo reliably runs on review day

## References (verified — cite these in reports/docs, don't invent others)

1. García-Feal, O. et al. (2022). Comparison of machine learning techniques for
   reservoir outflow forecasting. *Nat. Hazards Earth Syst. Sci.*, 22, 3859–3874.
   https://doi.org/10.5194/nhess-22-3859-2022
2. Kratzert, F. et al. (2018). Rainfall–runoff modelling using LSTM networks.
   *Hydrol. Earth Syst. Sci.*, 22, 6005–6022.
   https://doi.org/10.5194/hess-22-6005-2018
3. Cunge, J. A. (1969). On the subject of a flood propagation computation method
   (Muskingum method). *J. Hydraulic Research*, 7(2), 205–230.
   https://doi.org/10.1080/00221686909500264
4. Labadie, J. W. (2004). Optimal operation of multireservoir systems: State-of-
   the-art review. *J. Water Resources Planning and Management*, 130(2), 93–111.
   https://doi.org/10.1061/(ASCE)0733-9496(2004)130:2(93)
5. Rougé, C. et al. (2021). Coordination and control: limits in standard
   representations of multi-reservoir operations in hydrological modeling.
   *Hydrol. Earth Syst. Sci.*, 25, 1365–1388.
   https://doi.org/10.5194/hess-25-1365-2021
6. Dhumal, H.T. et al. (2022). Effect of flood releases from reservoirs in
   Krishna basin of Maharashtra state. *Innovative Infrastructure Solutions*, 7(1).
   https://doi.org/10.1007/s41062-021-00678-8

## Status

Proposal document finalized and submitted through the college ERI channel;
approved to begin build. This repo is the start of implementation.

## Notes for Claude Code

- Follow the scope boundaries above strictly — this is a semester project with a
  hard deadline; don't suggest scope expansions (Karnataka/Almatti, RL, full
  hydrodynamics) unless the user explicitly asks to discuss future work.
- When generating any user-facing text (README, dashboard copy, report drafts),
  keep the "advisory only, human decides" framing and the "reduces dam-attributable
  peak, doesn't prevent the flood" framing intact — these are deliberate, reviewed
  positions, not casual wording.
- Build order should roughly follow the module list above — routing before the ML
  forecaster, both before the advisor logic, dashboard last.
