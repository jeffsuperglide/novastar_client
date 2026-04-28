"""Test for Stations"""

from dataclasses import asdict
from typing import Dict, List
from unittest.mock import MagicMock

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models import TimeSeries, TimeSeriesResponse

from novastar_client.models.timeseries import TimeSeriesPoint
from tests.ts_data_54_5400 import ts_data


def test_timeseries_list_returns_timeseries_models():
    config = NovaStarConfig(api_version="v1")
    client = NovaStarClient(config)

    # mock_response = MagicMock()
    # mock_response.json.return_value = ts_data

    mock_get = MagicMock(return_value=ts_data)

    client.session.get = mock_get  # type: ignore[attr-defined]

    result: TimeSeriesResponse = client.timeseries.get(
        tsid="54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour"
    )

    ts: TimeSeries = result.timeseries
    ts_data_point: TimeSeriesPoint = ts.data[0]
    # ts_point_asdict: Dict = asdict(ts_data_point)

    assert isinstance(result, TimeSeriesResponse)
    assert isinstance(ts, TimeSeries)
    assert isinstance(ts_data_point, TimeSeriesPoint)
    assert result.timeseries.loc_id == "54-5400"
    assert result.timeseries.description == "Gatun promedio niveles"

    mock_get.assert_called_once()
    called_path, called_kwargs = mock_get.call_args
    assert called_path[0] == "ts"
    assert (
        called_kwargs["params"]["tsid"]
        == "54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour"
    )
