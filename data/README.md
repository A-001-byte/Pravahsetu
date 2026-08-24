# Data sources log

Log every raw file pulled into `data/raw/` or `data/events/` here: source
URL, date accessed, and what fields you got. Per the team's execution-plan
doc — you *will* forget where a CSV came from in three weeks otherwise.

| Date accessed | Source URL | Dam/gauge | Fields | Date range covered | Saved to | Notes |
|---|---|---|---|---|---|---|
| 2026-08-25 | cwc.gov.in/en/reservoir-level-storage-bulletin | Koyna | reservoir level (m), FRL (m), live storage (BCM), storage %age of FRL (current/last year/10yr avg) | week ending 22-07-2021 | `data/raw/koyna/cwc_bulletins/22072021-bulletin.pdf` | Parsed by `parse_cwc_bulletin()`. Koyna only -- CWC's national list doesn't include Warna/Radhanagari. No inflow/outflow in this source. |
| 2026-08-25 | cwc.gov.in/en/reservoir-level-storage-bulletin | Koyna | same as above | week ending 29-07-2021 | `data/raw/koyna/cwc_bulletins/29072021.pdf` | Same limitations as above. |
| 2026-08-25 | cwc.gov.in/en/reservoir-level-storage-bulletin | Koyna | same as above | week ending 05-08-2021 | `data/raw/koyna/cwc_bulletins/05082021-bulletin.pdf` | Same limitations as above. |
| 2026-08-25 | cwc.gov.in/en/reservoir-level-storage-bulletin | Koyna | same as above | week ending 12-08-2021 | `data/raw/koyna/cwc_bulletins/12.08.2021-ful-bull.pdf` | Same limitations as above. |
| 2026-08-25 | cwc.gov.in/en/reservoir-level-storage-bulletin | Koyna | same as above | week ending 08-08-2019 | `data/raw/koyna/cwc_bulletins/08.08.2019-cwc-bull.pdf` | Koyna at 100% capacity, level (658.88m) above FRL (657.90m) -- consistent with the 2019 flood peak. |
| 2026-08-25 | cwc.gov.in/en/reservoir-level-storage-bulletin | Koyna | same as above | week ending 14-08-2019 | `data/raw/koyna/cwc_bulletins/14.08.2019-cwc-bull.pdf` | Still ~100% capacity, recession phase. |

## Expected raw folders (already scaffolded, gitignored)

- `data/raw/koyna/`, `data/raw/warna/`, `data/raw/radhanagari/` — inflow, outflow, storage/level per dam
- `data/raw/gauges/` — downstream river gauge readings (e.g. Rajaram Weir, Sangli)
- `data/raw/rainfall/` — catchment rainfall
- `data/events/2019/`, `data/events/2021/` — the specific flood-window extracts used for Muskingum calibration and backtesting

## Primary sources (per CLAUDE.md and the team's execution-plan doc)

- **India-WRIS** (india-wris.gov.in) — register, search "Koyna" / "Warna" / "Radhanagari" in the reservoir/river monitoring section. Note the actual date range each export covers — it's often only the last few years, not back to 2019 in one file.
- **CWC** (cwc.gov.in) — weekly reservoir bulletins (published every Thursday), PDF, national list -- covers Koyna only, not Warna or Radhanagari, and has no inflow/outflow. Save every PDF into a `cwc_bulletins/` subfolder under the relevant `data/raw/<dam>/` folder.
- **IMD** (imdpune.gov.in) — gridded rainfall (0.25°) for the Sahyadri catchments. If registration is slow, use **Bhuvan** or **NASA GPM IMERG** rainfall as a stopgap (freely downloadable, no registration wait).
- **Flood-committee report + Dhumal et al. (2022)** (already in CLAUDE.md's references) — the source for the *actual* 2019/2021 release timeline. Extract by hand into a spreadsheet: date, time, dam, release rate — this is what the Module 5 backtest validates against, treat it as a first-class deliverable.
