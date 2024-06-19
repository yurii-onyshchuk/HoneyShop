import json
import requests

from django.conf import settings


class AbstractNovaPoshtaAPIRetriever:
    """Abstract class for fetching data from an external API.

    Contains common methods and properties for all weather data retrieval classes.
    """

    api_key = settings.NOVA_POSHTA_API_KEY
    api_url = settings.NOVA_POSHTA_API_URL

    def __init__(self, data: dict):
        self.data = data

    def get_response(self) -> dict:
        """Send a request to the external API and return the response."""
        request_data = self.get_request_data()
        response = post_request_to_api(self.api_url, request_data)
        return response

    def get_request_data(self) -> dict:
        """Define query parameters for the API request."""
        request_data = {'apiKey': self.api_key}
        return request_data


class CitySearcher(AbstractNovaPoshtaAPIRetriever):
    """Class to search for city names and retrieve city-related data from an external API."""

    def get_request_data(self) -> dict:
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

    def get_data_from_API(self) -> dict:
        """Fetch city name suggestions based on user input.

        This method queries an external API to retrieve city name
        suggestions matching the user's input.
        """
        return self.get_response()


def post_request_to_api(url: str, request_data: dict):
    """Send a request to an external API and return the response"""
    response = requests.post(url=url, json=request_data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise response.raise_for_status()
