"""Ingest historical inflow, outflow (gate discharge), and reservoir-level
records for Koyna, Warna, and Radhanagari.

Implemented so far: CWC weekly bulletin parsing. Two real limitations,
confirmed against six actual bulletins (22/29-Jul-2021, 05/12-Aug-2021,
08/14-Aug-2019):

  - CWC's national "130 important reservoirs" list includes Koyna but NOT
    Warna or Radhanagari (both too small for the national list).
  - CWC bulletins report reservoir level and live storage only -- no
    inflow/outflow (gate discharge) at all.

So this module currently gets Koyna level/storage only. Warna,
Radhanagari, and inflow/outflow for all three dams need a different
source (India-WRIS / Maharashtra WRD) -- see data/README.md.

Expected raw files: data/raw/koyna/cwc_bulletins/*.pdf
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import pdfplumber

# CWC's weekly bulletin spells it "KOYANA"; some IMD/state sources spell it
# "KOYNA". Match either. WARNA/RADHANAGARI are included for when a source
# that does cover them uses the same table layout -- they won't match
# today's CWC bulletins, which simply don't have those rows.
_ROW_PATTERN = re.compile(
    r"\*?(?P<sno>\d+)\s*(?P<dam>KOY[AN]{2,3}A?|WARNA|RADHANAGARI)\s+"
    r"(?P<frl_m>[\d.]+)\s+(?P<level_m>[\d.]+)\s+"
    r"(?P<capacity_bcm>[\d.]+)\s+(?P<storage_bcm>[\d.]+)\s+"
    r"(?P<obs_date>\d{2}-\d{2}-\d{2,4})\s+"
    r"(?P<pct_current>\d+)\s+(?P<pct_last_year>\d+)\s+(?P<pct_10yr_avg>\d+)"
)


@dataclass(frozen=True)
class CwcBulletinRow:
    """One dam's row from a CWC 'Weekly Report of Important Reservoirs' bulletin."""

    dam: str
    obs_date: date
    frl_m: float
    reservoir_level_m: float
    live_capacity_bcm: float
    live_storage_bcm: float
    pct_of_frl_current_year: int
    pct_of_frl_last_year: int
    pct_of_frl_10yr_avg: int


def _parse_bulletin_date(raw: str) -> date:
    """CWC bulletins mix DD-MM-YYYY and DD-MM-YY across issues."""
    for fmt in ("%d-%m-%Y", "%d-%m-%y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unrecognized CWC bulletin date format: {raw!r}")


def _normalize_dam_name(raw: str) -> str:
    return "Koyna" if raw.upper().startswith("KOY") else raw.title()


def parse_cwc_bulletin(pdf_path: Path) -> list[CwcBulletinRow]:
    """Extract per-dam rows from one CWC weekly reservoir bulletin PDF.

    Only returns rows CWC's national list actually has -- in practice
    that means Koyna only (see module docstring). Each bulletin also has
    a second, wider table later on with the same dams in a different
    column order (state + benefits columns inserted before the numbers);
    this regex is deliberately shaped to match only the first, narrower
    table, so dams aren't double-counted from that second table.
    """
    rows: list[CwcBulletinRow] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.split("\n"):
                match = _ROW_PATTERN.search(line)
                if not match:
                    continue
                rows.append(
                    CwcBulletinRow(
                        dam=_normalize_dam_name(match.group("dam")),
                        obs_date=_parse_bulletin_date(match.group("obs_date")),
                        frl_m=float(match.group("frl_m")),
                        reservoir_level_m=float(match.group("level_m")),
                        live_capacity_bcm=float(match.group("capacity_bcm")),
                        live_storage_bcm=float(match.group("storage_bcm")),
                        pct_of_frl_current_year=int(match.group("pct_current")),
                        pct_of_frl_last_year=int(match.group("pct_last_year")),
                        pct_of_frl_10yr_avg=int(match.group("pct_10yr_avg")),
                    )
                )
    return rows


def parse_cwc_bulletins(pdf_dir: Path) -> list[CwcBulletinRow]:
    """Parse every *.pdf in a folder (e.g. data/raw/koyna/cwc_bulletins/)."""
    rows: list[CwcBulletinRow] = []
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        rows.extend(parse_cwc_bulletin(pdf_path))
    return rows


# TODO: Warna, Radhanagari, and inflow/outflow (all three dams) need a
# loader against India-WRIS or Maharashtra WRD exports once that data is
# in hand -- CWC bulletins structurally cannot provide them. See
# data/README.md.
