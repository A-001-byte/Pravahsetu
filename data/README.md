# Data sources log

Log every raw file pulled into `data/raw/` or `data/events/` here: source
URL, date accessed, and what fields you got. Per the team's execution-plan
doc — you *will* forget where a CSV came from in three weeks otherwise.

| Date accessed | Source URL | Dam/gauge | Fields | Date range covered | Saved to | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

## Expected raw folders (already scaffolded, gitignored)

- `data/raw/koyna/`, `data/raw/warna/`, `data/raw/radhanagari/` — inflow, outflow, storage/level per dam
- `data/raw/gauges/` — downstream river gauge readings (e.g. Rajaram Weir, Sangli)
- `data/raw/rainfall/` — catchment rainfall
- `data/events/2019/`, `data/events/2021/` — the specific flood-window extracts used for Muskingum calibration and backtesting

## Primary sources (per CLAUDE.md and the team's execution-plan doc)

- **India-WRIS** (india-wris.gov.in) — register, search "Koyna" / "Warna" / "Radhanagari" in the reservoir/river monitoring section. Note the actual date range each export covers — it's often only the last few years, not back to 2019 in one file.
- **CWC** (cwc.gov.in) — daily reservoir bulletins, often PDF. Save every PDF into a `cwc_bulletins/` subfolder under the relevant `data/raw/<dam>/` folder.
- **IMD** (imdpune.gov.in) — gridded rainfall (0.25°) for the Sahyadri catchments. If registration is slow, use **Bhuvan** or **NASA GPM IMERG** rainfall as a stopgap (freely downloadable, no registration wait).
- **Flood-committee report + Dhumal et al. (2022)** (already in CLAUDE.md's references) — the source for the *actual* 2019/2021 release timeline. Extract by hand into a spreadsheet: date, time, dam, release rate — this is what the Module 5 backtest validates against, treat it as a first-class deliverable.
