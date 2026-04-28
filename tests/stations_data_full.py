"""Testing Payloads"""

from typing import Dict, Any


stations_full: Dict[str, Any] = {
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
