"""Test for Stations"""

from typing import Any, List
from unittest.mock import MagicMock

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models import TimeSeries, TimeSeriesResponse

from novastar_client.models.timeseries import TimeSeriesPoint
from novastar_client.tests.ts_data_54_5400 import ts_data


def test_timeseries_list_returns_timeseries_models():
    config = NovaStarConfig(api_version="v1")
    client = NovaStarClient(config)

    mock_response = MagicMock()
    mock_response.json.return_value = ts_data

    mock_get = MagicMock(return_value=mock_response)

    client.session.get = mock_get  # type: ignore[attr-defined]

    result = client.timeseries.get(tsid="54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour")

    assert isinstance(result, TimeSeriesResponse)
    assert isinstance(result.timeseries, TimeSeries)
    assert isinstance(result.timeseries.data, List)
    # assert result.timeseries.loc_id == "54-5400"
    # assert result.timeseries.description == "Gatun promedio niveles"

    # mock_get.assert_called_once()
    # called_path, called_kwargs = mock_get.call_args
    # assert called_path[0] == "ts"
    # assert (
    #     called_kwargs["params"]["tsid"]
    #     == "54-5400.NovaStar5.WaterLevelRiver-Mean.1Hour"
    # )
