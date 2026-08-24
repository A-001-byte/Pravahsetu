"""Tests for CWC bulletin parsing. Uses a synthetic line matching the real
public-bulletin format (not a copy of any actual downloaded PDF).
"""

import re

from pravaha_setu.data_pipeline.ingest.reservoir_data import _ROW_PATTERN, _parse_bulletin_date


def test_row_pattern_matches_a_koyna_style_line() -> None:
    # Arrange -- format mirrors CWC's real "WEEKLY REPORT OF ... RESERVOIRS" table
    line = "*47 KOYANA 657.90 648.08 2.652 1.745 22-07-2021 66 47 57 0 1920"

    # Act
    match = _ROW_PATTERN.search(line)

    # Assert
    assert match is not None
    assert match.group("dam") == "KOYANA"
    assert match.group("frl_m") == "657.90"
    assert match.group("level_m") == "648.08"
    assert match.group("storage_bcm") == "1.745"
    assert match.group("obs_date") == "22-07-2021"


def test_row_pattern_handles_sno_glued_to_dam_name() -> None:
    # Arrange -- some bulletins have no space between "*41" and "KOYANA"
    line = "*41KOYANA 657.90 658.88 2.652 2.652 08-08-2019 100 94 87 - 1920"

    # Act
    match = _ROW_PATTERN.search(line)

    # Assert
    assert match is not None
    assert match.group("storage_bcm") == "2.652"


def test_parse_bulletin_date_handles_two_and_four_digit_years() -> None:
    assert _parse_bulletin_date("14-08-2019").isoformat() == "2019-08-14"
    assert _parse_bulletin_date("14-08-19").isoformat() == "2019-08-14"
