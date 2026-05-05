"""Test for Stations"""

from unittest.mock import MagicMock

from novastar_client import NovaStarClient, NovaStarConfig
from novastar_client.models import DataType, DataTypeResponse

from tests.datatypes_shef import datatypes


def test_datatype_list_returns_datatype_models():
    config = NovaStarConfig(api_version="v1")
    client = NovaStarClient(config)

    # mock_response = MagicMock()
    # mock_response.json.return_value = ts_data

    mock_get = MagicMock(return_value=datatypes)

    client.session.get = mock_get  # type: ignore[attr-defined]

    resp: DataTypeResponse | None = client.datatypes.get(
        sort="-name",
        shefPhysicalElement="H*",
    )

    data: list[DataType] = resp.datatypes # type: ignore

    assert isinstance(resp, DataTypeResponse)
    assert isinstance(data[0], DataType)

    mock_get.assert_called_once()
    called_path, called_kwargs = mock_get.call_args
    assert called_path[0] == "dataTypes"
    assert called_kwargs["params"]["sort"] == "-name"
    assert called_kwargs["params"]["shefPhysicalElement"] == "H*"
