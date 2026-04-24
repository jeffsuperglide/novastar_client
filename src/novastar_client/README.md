# novastar-client

`novastar-client` is a Python client for NovaStar-style REST data endpoints exposed under paths like:

- `/novastar/data/api/v1/stations`
- `/novastar/data/api/v1/time-series`
- `/novastar/data/api/v1/ratings`
- `/novastar/data/api/v1/points`
- `/novastar/data/api/v1/general`

It provides:

- A version-aware client (`v1`, `v2`, etc.) using a configurable `api_version`
- Grouped services (Stations, Time Series, Ratings, Points, General)
- Typed models for resources (starting with Stations), including support for both `jsonFormat=full` and `jsonFormat=bare` response shapes


## Features

- **Versioned API root**: Requests go to `/novastar/data/api/{api_version}/...` based on configuration.
- **Grouped endpoints**: Access resources via `client.stations`, `client.time_series`, `client.ratings`, `client.points`, and `client.general`.
- **Stations models**:
  - `jsonFormat=bare`: top-level JSON is an array of station objects.
  - `jsonFormat=full`: top-level JSON is an envelope with `apiVersion`, `attributionAndUsage`, `responseInfo`, and `stations`.
- **Editable install**: Designed for `pip install -e .` so you can iterate quickly while developing.


## Installation (local editable)

Create a virtual environment and install the package in editable mode:

```bash
# from the repository root (where pyproject.toml lives)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -e ".[dev]"
```

This will:

- Install `novastar-client` in editable mode
- Install dev tools like `pytest` (defined under `[project.optional-dependencies].dev` in `pyproject.toml`)


## Configuration

The client configuration is defined via `NovaStarConfig`:

```python
from novastar_client import NovaStarClient, NovaStarConfig

config = NovaStarConfig(
    base_url="https://panama-cloud-ns5.trilynx-novastar.systems",
    api_version="v1",  # or "v2" when you support it
    timeout=30,
    verify_ssl=True,
)

client = NovaStarClient(config)
```

Key options:

- `base_url`: Root of the NovaStar deployment
- `api_version`: Version segment used in the URL, e.g. `"v1"` → `/novastar/data/api/v1/...`
- `timeout`: Request timeout in seconds
- `verify_ssl`: SSL verification toggle


## Client structure

The top-level client wires a shared HTTP session into category-specific services:

```python
from novastar_client import NovaStarClient, NovaStarConfig

client = NovaStarClient(NovaStarConfig(api_version="v1"))

# Services
stations_service = client.stations
# (time_series, ratings, points, general can be added similarly)
```


## Stations API

The `StationsAPI` exposes a `list` method that maps directly to the `stations` endpoint and supports both `jsonFormat=full` and `jsonFormat=bare`.

### Parameters

The following query parameters are supported:

- `station_num_ids` → `stationNumId` (comma-separated list)
- `station_name` → `stationName` (supports `*` wildcard at start and/or end)
- `include_retired_stations` → `includeRetiredStations`
- `include_test_stations` → `includeTestStations`
- `debug` → `debug`
- `json_format` → `jsonFormat` (`"full"` or `"bare"`)
- `xml_format` → `xmlFormat`
- `format_pretty_print` → `formatPrettyPrint`

### jsonFormat=bare

When `json_format="bare"`, the endpoint returns a JSON array of station objects, and the client returns a `List[Station]`.

```python
from novastar_client import NovaStarClient, NovaStarConfig

client = NovaStarClient(NovaStarConfig(api_version="v1"))

stations = client.stations.list(
    station_num_ids=,[1][2]
    json_format="bare",
)

for s in stations:
    print(s.num_id, s.name, s.latitude, s.longitude)
```

`Station` fields (derived from the bare JSON) include:

- `id: int`
- `num_id: int` (from `numId`)
- `name: str`
- `description: Optional[str]`
- `description_text: Optional[str]`
- `dashboard_url: Optional[str]`
- `elevation: Optional[float]`
- `last_time_polled: Optional[str]`
- `latitude: Optional[float]`
- `longitude: Optional[float]`
- `out_of_service: Optional[bool]`
- `remote_tag: Optional[str]`
- `retired_station: Optional[bool]`
- `tag_name: Optional[str]`
- `test_station: Optional[bool]`
- `type_id: Optional[int]`
- `station_type_name: Optional[str]`
- `station_type_protocol: Optional[str]`


### jsonFormat=full

When `json_format="full"`, the endpoint returns a structured envelope with version metadata, attribution/usage info, response info, and a `stations` array. The client returns a `StationsResponse` model.

```python
resp = client.stations.list(
    station_name="*PANAMA*",
    json_format="full",
)

print(resp.api_version.api_dot_delimited_version)
print(resp.response_info.size)
for s in resp.stations:
    print(s.num_id, s.name)
```

`StationsResponse` contains:

- `api_version: ApiVersion`
- `attribution_and_usage: AttributionAndUsage`
- `response_info: ResponseInfo`
- `stations: List[Station]`

This lets you access both the actual station data and useful metadata such as query timing, caching, and attribution requirements.


## Models

Models live under `src/novastar_client/models/` and are responsible for mapping API JSON into typed Python objects.

Currently implemented:

- `Station`: one station record
- `StationsResponse`: full envelope for the stations endpoint
- `ApiVersion`, `AttributionAndUsage`, `ResponseInfo`: envelope metadata

Each model provides a `from_api` class method to construct it from a raw `dict`:

```python
from novastar_client.models import Station, StationsResponse

station = Station.from_api(raw_station_dict)
stations_response = StationsResponse.from_api(raw_envelope_dict)
```


## Running tests

Tests use `pytest` and mock the HTTP session so you can verify behavior without hitting a real NovaStar instance.

To run all tests:

```bash
pytest
```

### Example: test for Stations API

The `tests/test_stations_api.py` file exercises both `jsonFormat=bare` and `jsonFormat=full` behavior:

- Ensures the correct query parameter (`jsonFormat`) is sent.
- Asserts that `json_format="bare"` returns a `List[Station]`.
- Asserts that `json_format="full"` returns a `StationsResponse`.

A simplified example:

```python
from typing import Any
from unittest.mock import MagicMock

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models import Station, StationsResponse


def test_stations_list_bare_returns_station_models():
    bare_payload = [
        {
            "id": 1,
            "numId": 123,
            "name": "TEST STATION",
            "description": "",
            "descriptionText": "",
            "dashboardUrl": None,
            "elevation": 10.5,
            "lastTimePolled": "2024-01-01T00:00:00-05:00",
            "latitude": 9.0,
            "longitude": -79.5,
            "outOfService": False,
            "remoteTag": "123",
            "retiredStation": False,
            "tagName": "TST",
            "testStation": False,
            "typeId": 20,
            "stationTypeName": "Campbell Scientific ALERT2 Radio",
            "stationTypeProtocol": "ALERT2",
        }
    ]

    config = NovaStarConfig(api_version="v1")
    client = NovaStarClient(config)

    mock_get = MagicMock(return_value=bare_payload)
    client.session.get = mock_get  # type: ignore[attr-defined]

    result = client.stations.list(json_format="bare")

    assert isinstance(result, list)
    assert isinstance(result, Station)
    assert result.num_id == 123
    assert result.name == "TEST STATION"

    called_path, called_kwargs = mock_get.call_args
    assert called_path == "stations"
    assert called_kwargs["params"]["jsonFormat"] == "bare"


def test_stations_list_full_returns_stations_response():
    full_payload: dict[str, Any] = {
        "apiVersion": {
            "apiVersionMajor": "1",
            "apiVersionMinor": "0",
            "apiVersionMicro": "0",
            "apiVersionModifier": "",
            "apiVersionDate": "2024-01-01",
            "apiVersionTime": "00:00:00",
            "apiDotDelimitedVersion": "1.0.0",
        },
        "attributionAndUsage": {
            "providerOrganizationText": "Test Org",
            "providerOrganizationUri": "https://example.com",
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
            "urlOriginal": "https://example.com",
            "urlOriginalEncoded": "",
            "url": "",
            "urlEncoded": "",
            "periodStart": None,
            "periodEnd": None,
            "size": 1,
            "queryStart": "2024-01-01T00:00:00Z",
            "queryMs": 10,
            "queryTargetMs": 50,
            "queryTargetMet": True,
            "isCached": False,
            "cacheExpirationTime": None,
        },
        "stations": bare_payload,
    }

    config = NovaStarConfig(api_version="v1")
    client = NovaStarClient(config)

    mock_get = MagicMock(return_value=full_payload)
    client.session.get = mock_get  # type: ignore[attr-defined]

    result = client.stations.list(json_format="full")

    assert isinstance(result, StationsResponse)
    assert result.api_version.api_dot_delimited_version == "1.0.0"
    assert len(result.stations) == 1
    assert result.stations.name == "TEST STATION"

    called_path, called_kwargs = mock_get.call_args
    assert called_path == "stations"
    assert called_kwargs["params"]["jsonFormat"] == "full"
```


## Roadmap

- Add service modules and models for:
  - Time Series
  - Ratings
  - Points
  - General (health, info, etc.)
- Introduce version strategies for `v2` when the API contract diverges from `v1` while keeping the Python interface stable.
- Optional: add higher-level helpers (e.g., “get latest measurement for station X and point Y”) on top of the raw endpoints.


## License

TBD (add your preferred license here).