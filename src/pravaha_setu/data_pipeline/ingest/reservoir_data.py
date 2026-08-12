"""Ingest historical inflow, outflow (gate discharge), and reservoir-level
records for Koyna, Warna, and Radhanagari.

Expected sources: India-WRIS, Central Water Commission, Maharashtra Water
Resources Department (see CLAUDE.md > Resources Required > Datasets).
Raw files are expected under data/raw/<dam_name>/.

TODO (Module 1): implement loader(s) that read raw exports (CSV/Excel) into
a common schema and return pandas DataFrames, e.g.:
    def load_reservoir_timeseries(dam: str, raw_dir: Path) -> pd.DataFrame
"""
