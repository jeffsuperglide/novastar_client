"""Test for Stations"""

from typing import Any
from unittest.mock import MagicMock

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models import Station, StationsResponse


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
    bare_payload = [
        {
            "id": 226,
            "numId": 1,
            "name": "AAA ESTACION DE PRUEBA",
            "description": 'Estacion Campbell  "DE PRUEBA" instalada el 9 de abril del 2019, consiste de un TB y un logger alimentado de energia solar ademas sensor de viento',
            "descriptionText": 'Estacion Campbell  "DE PRUEBA" instalada el 9 de abril del 2019, consiste de un TB y un logger alimentado de energia solar ademas sensor de viento',
            "dashboardUrl": None,
            "elevation": 95,
            "lastTimePolled": "1980-01-01T00:00:00-05:00",
            "latitude": 9.211,
            "longitude": -79.917,
            "outOfService": False,
            "remoteTag": "1",
            "retiredStation": False,
            "tagName": "TESTCAMP",
            "testStation": False,
            "typeId": 20,
            "stationTypeName": "Campbell Scientific ALERT2 Radio",
            "stationTypeProtocol": "ALERT2",
        }
    ]

    client, mock_get = make_client_with_mocked_session(
        bare_payload=bare_payload, full_payload=None
    )

    result = client.stations.get(json_format="bare")

    assert isinstance(result, StationsResponse)
    assert isinstance(result.stations, Station)
    assert result.stations[0].num_id == 1
    assert result.stations[0].name == "AAA ESTACION DE PRUEBA"

    mock_get.assert_called_once()
    called_path, called_kwargs = mock_get.call_args
    assert called_path[0] == "stations"
    assert called_kwargs["params"]["jsonFormat"] == "bare"


def test_stations_list_full_returns_stations_response():
    full_payload = {
        "apiVersion": {
            "apiVersionMajor": "1",
            "apiVersionMinor": "13",
            "apiVersionMicro": "1",
            "apiVersionModifier": "",
            "apiVersionDate": "2025-08-15",
            "apiVersionTime": "",
            "apiDotDelimitedVersion": "1.13.1",
        },
        "attributionAndUsage": {
            "providerOrganizationText": "",
            "providerOrganizationUri": "",
            "dataPolicyUri": "",
            "disclaimerText": "",
            "disclaimerUri": "",
            "licenseText": "",
            "licenseUri": "",
            "usageConstraintsText": "",
            "usageConstraintsUri": "",
            "recommendedAttributionText": "",
        },
        "responseInfo": {
            "urlOriginal": "http://panama-cloud-ns5.trilynx-novastar.systems/novastar-data/api/v1/stations?debug=false&format=json&formatPrettyPrint=true&includeRetiredStations=false&includeTestStations=false&jsonFormat=full&stationNumId=1&xmlFormat=full",
            "urlOriginalEncoded": "http://panama-cloud-ns5.trilynx-novastar.systems/novastar-data/api/v1/stations?debug=false&format=json&formatPrettyPrint=true&includeRetiredStations=false&includeTestStations=false&jsonFormat=full&stationNumId=1&xmlFormat=full",
            "url": "http://localhost/novastar-data/api/v1/stations?debug=false&format=json&formatPrettyPrint=true&includeRetiredStations=false&includeTestStations=false&jsonFormat=full&stationNumId=1&xmlFormat=full",
            "urlEncoded": "http://localhost/novastar-data/api/v1/stations?debug=false&format=json&formatPrettyPrint=true&includeRetiredStations=false&includeTestStations=false&jsonFormat=full&stationNumId=1&xmlFormat=full",
            "periodStart": None,
            "periodEnd": None,
            "size": 1,
            "queryStart": "2026-04-24T11:32:47.652093-05:00",
            "queryMs": 1,
            "queryTargetMs": -999,
            "queryTargetMet": None,
            "isCached": False,
            "cacheExpirationTime": None,
        },
        "stations": [
            {
                "id": 226,
                "numId": 1,
                "name": "AAA ESTACION DE PRUEBA",
                "description": 'Estacion Campbell  "DE PRUEBA" instalada el 9 de abril del 2019, consiste de un TB y un logger alimentado de energia solar ademas sensor de viento',
                "descriptionText": 'Estacion Campbell  "DE PRUEBA" instalada el 9 de abril del 2019, consiste de un TB y un logger alimentado de energia solar ademas sensor de viento',
                "dashboardUrl": None,
                "elevation": 95,
                "lastTimePolled": "1980-01-01T00:00:00-05:00",
                "latitude": 9.211,
                "longitude": -79.917,
                "outOfService": False,
                "remoteTag": "1",
                "retiredStation": False,
                "tagName": "TESTCAMP",
                "testStation": False,
                "typeId": 20,
                "stationTypeName": "Campbell Scientific ALERT2 Radio",
                "stationTypeProtocol": "ALERT2",
            }
        ],
    }

    client, mock_get = make_client_with_mocked_session(
        bare_payload=None, full_payload=full_payload
    )

    result = client.stations.get(json_format="full")

    assert isinstance(result, StationsResponse)
    assert result.api_version.api_dot_delimited_version == "1.13.1"
    assert len(result.stations) == 1
    assert result.stations[0].name == "AAA ESTACION DE PRUEBA"

    mock_get.assert_called_once()
    called_path, called_kwargs = mock_get.call_args
    assert called_path[0] == "stations"
    assert called_kwargs["params"]["jsonFormat"] == "full"
