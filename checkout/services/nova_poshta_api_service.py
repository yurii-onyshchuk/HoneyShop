import json
from abc import abstractmethod, ABC

import requests

from django.conf import settings


def post_request_to_api(url: str, request_data: dict):
    """Send a request to an external API and return the response"""
    response = requests.post(url=url, json=request_data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise response.raise_for_status()


class AbstractNovaPoshtaAPIRetriever(ABC):
    """Abstract class for fetching data from an external API.

    Contains common methods and properties for all weather data retrieval classes.
    """

    api_key = settings.NOVA_POSHTA_API_KEY
    api_url = settings.NOVA_POSHTA_API_URL

    def __init__(self, data: dict):
        self.data = data

    @abstractmethod
    def query_params(self, **kwargs) -> dict:
        """Define query parameters for the API request."""
        pass

    def get_response_from_API(self) -> dict:
        """Fetch city name suggestions based on user input.

        This method queries an external API to retrieve city name
        suggestions matching the user's input.
        """
        response = post_request_to_api(self.api_url, self.query_params())
        return response


class CitySearcher(AbstractNovaPoshtaAPIRetriever):
    """Class to search for city names and retrieve city-related data from an external API."""

    def query_params(self) -> dict:
        request_data = {
            "apiKey": f"{self.api_key}",
            "modelName": "Address",
            "calledMethod": "searchSettlements",
            "methodProperties": {
                "CityName": f"{self.data['city']}",
                "Limit": "10",
                "Page": "1"
            }
        }
        return request_data


class DepartmentSearcher(AbstractNovaPoshtaAPIRetriever):
    def query_params(self) -> dict:
        request_data = {
            "apiKey": f"{self.api_key}",
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityRef": self.data['city_id'],
                "FindByString": self.data['query'],
                "Language": "UA",
                "Limit": "10",
                "Page": "1"
            }
        }
        return request_data
