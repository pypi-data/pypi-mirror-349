import asyncio
from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import AsyncMock, patch
import json

import aiohttp

RESP_142 =  json.loads("""{"stationId":142,"stationName":"THPK Ersfjord","location":{"latitude":"69.70017",
"longitude":"18.63842","altitude":130},"dateTime":"2025-05-19 15:45:00","wind":{"speed":9.4,"gust":13.3,"min":0,
"unit":"m/s","direction":245},"battery":4.15,"daily":{"max_temp":0,"min_temp":0},"temperature":0}""")

RESP_ALL = json.loads("""{"measurements":[{"stationId":142,"stationName":"THPK Ersfjord","location":{"latitude":"69.70017",
"longitude":"18.63842","altitude":130},"dateTime":"2025-05-19 15:45:00","wind":{"speed":9.4,"gust":13.3,"min":0,
"unit":"m/s","direction":245},"battery":4.15,"daily":{"max_temp":0,"min_temp":0},"temperature":0},
{"stationId":207,"stationName":"THPK Finnvikdalen","location":{"latitude":"69.76117",
"longitude":"18.85657","altitude":270},"dateTime":"2025-05-19 15:45:00",
"wind":{"speed":10,"gust":13.6,"min":0,"unit":"m/s","direction":339},"battery":4.14,
"daily":{"max_temp":7.5,"min_temp":4.5},"temperature":4.7},{"stationId":299,"stationName":"THPK Fjellheisen",
"location":{"latitude":"69.63116","longitude":"18.99377","altitude":420},"dateTime":"2025-05-19 15:45:00",
"wind":{"speed":7.8,"gust":10.3,"min":0,"unit":"m/s","direction":256},"battery":4.14,
"daily":{"max_temp":5.7,"min_temp":0},"temperature":3.6}]}""")

RESP_AUTHERROR=json.loads("""
{"measurements":[{"stationId":105,"error":"Sorry, you don't have access for this station.","errorCode":"no_access"},
{"stationId":106,"error":"Sorry, you don't have access for this station.","errorCode":"no_access"}]}""")

from holfuy import HolfuyService

from holfuy.const import (
    CONF_TEMPERATURE_UNIT_CELSIUS,
    CONF_WIND_SPEED_UNIT_MS,
    CONF_AVERAGING_NEWEST,
)


class TestHolfuyService(IsolatedAsyncioTestCase):
    def setUp(self):
        """Set up test cases."""
        self.session = AsyncMock(spec=aiohttp.ClientSession)
        self.api = HolfuyService(
            "test_api_key",
            self.session,
            CONF_TEMPERATURE_UNIT_CELSIUS,
            CONF_WIND_SPEED_UNIT_MS,
            False,
        )

    async def test_fetch_data_single_station(self):
        """Test fetching data for a single station."""
        mock_response = RESP_142

        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_response)

        self.session.get = AsyncMock(return_value=mock_resp)

        result = await self.api.fetch_data(["142"])

        expected_params = {
            "pw": "test_api_key",
            "m": "JSON",
            "tu": CONF_TEMPERATURE_UNIT_CELSIUS,
            "su": CONF_WIND_SPEED_UNIT_MS,
            "avg": CONF_AVERAGING_NEWEST,
            "s": "142",
        }

        self.session.get.assert_called_once_with(
            "http://api.holfuy.com/live/",
            params=expected_params
        )

        self.assertEqual(result["measurements"][0]["stationId"], 142)

    async def test_fetch_data_all_stations(self):
        """Test fetching data for multiple stations."""
        mock_response = RESP_ALL

        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_response)
        self.session.get = AsyncMock(return_value= mock_resp)

        result = await self.api.fetch_data(None)

        expected_params = {
            "pw": "test_api_key",
            "m": "JSON",
            "tu": CONF_TEMPERATURE_UNIT_CELSIUS,
            "su": CONF_WIND_SPEED_UNIT_MS,
            "avg": CONF_AVERAGING_NEWEST,
            "s": "all",
        }

        self.session.get.assert_called_once_with(
            "http://api.holfuy.com/live/",
            params=expected_params
        )

        self.assertEqual(result, mock_response)

    async def test_fetch_data_error_response(self):
        """Test handling of error responses."""
        mock_resp = AsyncMock()
        mock_resp.status = 404

        self.session.get = AsyncMock(return_value=mock_resp)

        result = await self.api.fetch_data(None)

        self.assertIsNone(result)

    async def test_fetch_data_invalid_access_token(self):
        """Test handling of error responses."""
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_response =  RESP_AUTHERROR

        mock_resp.json = AsyncMock(return_value=mock_response)

        self.session.get = AsyncMock(return_value=mock_resp)

        result = await self.api.fetch_data(["105","106"])

        expected_params = {
            "pw": "test_api_key",
            "m": "JSON",
            "tu": CONF_TEMPERATURE_UNIT_CELSIUS,
            "su": CONF_WIND_SPEED_UNIT_MS,
            "avg": CONF_AVERAGING_NEWEST,
            "s": "105,106",
        }

        self.session.get.assert_called_once_with(
            "http://api.holfuy.com/live/",
            params=expected_params
        )

        self.assertEqual(result["measurements"][0]["stationId"], 105)

    async def test_fetch_data_timeout(self):
        """Test handling of timeout errors."""
        self.session.get = AsyncMock(side_effect=asyncio.TimeoutError)

        result = await self.api.fetch_data(None)

        self.assertIsNone(result)

    async def test_fetch_data_client_error(self):
        """Test handling of client errors."""
        self.session.get = AsyncMock(side_effect=aiohttp.ClientError)

        result = await self.api.fetch_data(None)

        self.assertIsNone(result)
