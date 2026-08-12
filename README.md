# Pravaha Setu

Coordinated flood-release advisory system for the Kolhapur and Sangli region,
Upper Krishna Basin, Maharashtra — a semester project at Vishwakarma
Institute of Technology, Department of Computer Engineering.

**Advisory only.** This system never operates dam gates. It forecasts
reservoir inflow, routes flood waves to Kolhapur/Sangli, and recommends a
staggered release schedule so peaks don't stack downstream — every release
decision stays with human operators and authorities.

- Full project context, scope, and tech stack: [CLAUDE.md](CLAUDE.md)
- Local setup instructions: [SETUP.md](SETUP.md)
- Original proposal: [Project_Proposal 2.pdf](Project_Proposal%202.pdf)

## Repository layout

```
src/pravaha_setu/    Python package: data pipeline, routing, forecasting,
                      advisor, and simulation/backtesting modules
backend/              FastAPI service (Module 6, not yet built)
frontend/             React + Vite dashboard (Module 6, not yet built)
data/                 Raw/processed data and event extracts (gitignored,
                      folder layout only — see SETUP.md > Data)
notebooks/            Exploratory backtesting notebooks only; final logic
                      lives in src/pravaha_setu, not notebooks
tests/                pytest suite, mirrors src/pravaha_setu
```

## Status

Repository scaffolding only — module implementation has not started yet.
Build order (see CLAUDE.md): data pipeline → routing → forecasting →
advisor → simulation/backtesting → dashboard/API.
