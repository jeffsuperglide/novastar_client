"""Tests for SHEF lookup methods"""

import builtins
from importlib import resources

import pytest

import novastar_client.data  # adjust if your package path differs
from novastar_client.transform.shef_lookup import (
    ShefCodeInfo,
    _data_lines,
    load_shef_map,
    get_shef_info,
)


def test_data_lines_skips_header_and_blank_lines(tmp_path, monkeypatch):
    # Build a fake file with 3 header lines, some blank lines, and data
    content = "\n".join(
        [
            "header line 1",
            "header line 2",
            "header line 3",
            "",
            "QS,Flow-Spillway,cfs,*,1000",
            "",
            "HG,Stage,ft,INST-VAL,1.0",
            "  ",  # whitespace-only line
            "QR,Discharge,cfs,INST-VAL,1.0",
            "",
        ]
    )

    p = tmp_path / "fake.csv"
    p.write_text(content, encoding="utf-8")

    with p.open() as f:
        # Skip the 3 header lines
        lines = list(_data_lines(f, skip=3))

    # Should include the header row and data rows, but no completely blank or whitespace-only lines
    assert lines == [
        "QS,Flow-Spillway,cfs,*,1000\n",
        "HG,Stage,ft,INST-VAL,1.0\n",
        "QR,Discharge,cfs,INST-VAL,1.0\n",
    ]


def test_load_shef_map_structure_and_types():
    shef_map = load_shef_map()

    # Basic properties
    assert isinstance(shef_map, dict)
    assert shef_map, "Expected non-empty shef map"

    # Pick one arbitrary entry and sanity-check its type and fields
    shef_code_info = shef_map["LA"]
    assert isinstance(shef_code_info, ShefCodeInfo)
    assert isinstance(shef_code_info.parameter, str)
    assert isinstance(shef_code_info.unit, str)
    assert isinstance(shef_code_info.data_type, str)
    # conversion type is Any, but the loader uses .strip(), so it must at least be a str
    assert isinstance(int(shef_code_info.conversion), int)


def test_get_shef_info_unknown_code():
    unknown_code = "ZZZ_UNKNOWN_CODE"

    with pytest.raises(KeyError) as excinfo:
        get_shef_info(unknown_code)

    msg = str(excinfo.value)
    # The raised KeyError should use the custom message
    assert f"Unknown shef code: {unknown_code}" in msg
