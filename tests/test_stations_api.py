"""Test for Stations"""

from typing import Any
from unittest.mock import MagicMock

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models import Station, StationResponse
from tests.stations_data_bare import stations_bare
from tests.stations_data_full import stations_full


def make_client_with_mocked_session(bare_payload: Any = None, full_payload: Any = None):
    config = NovaStarConfig(api_version="v1")
    client = NovaStarClient(config)

    mock_get = MagicMock()

    def get_side_effect(path: str, params: dict[str, Any]):
        json_format = params.get("jsonFormat", "full")
        if json_format == "bare":
            return bare_payload
        return full_payload

    mock_get.side_effect = get_side_effect
    client.session.get = mock_get  # type: ignore[attr-defined]

    return client, mock_get


def test_stations_list_bare_returns_station_models():
    bare_payload = stations_bare

    client, mock_get = make_client_with_mocked_session(
        bare_payload=bare_payload, full_payload=None
    )

    result = client.stations.get(jsonFormat="bare")

    assert isinstance(result, StationResponse)
    assert isinstance(result.stations[0], Station)
    assert result.stations[0].num_id == 1
    assert result.stations[0].name == "AAA ESTACION DE PRUEBA"

    mock_get.assert_called_once()
    called_path, called_kwargs = mock_get.call_args
    assert called_path[0] == "stations"
    assert called_kwargs["params"]["jsonFormat"] == "bare"


def test_stations_list_full_returns_stations_response():
    full_payload = stations_full

    client, mock_get = make_client_with_mocked_session(
        bare_payload=None, full_payload=full_payload
    )

    result = client.stations.get(jsonFormat="full")

    assert isinstance(result, StationResponse)
    assert result.api_version.api_dot_delimited_version == "1.13.1"
    assert len(result.stations) == 1
    assert result.stations[0].name == "AAA ESTACION DE PRUEBA"

    mock_get.assert_called_once()
    called_path, called_kwargs = mock_get.call_args
    assert called_path[0] == "stations"
    assert called_kwargs["params"]["jsonFormat"] == "full"
