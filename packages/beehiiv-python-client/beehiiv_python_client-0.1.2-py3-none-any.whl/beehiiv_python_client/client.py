import requests
from typing import Optional, Dict, Any

from .exceptions import (
    BeehiivAPIException,
    BeehiivRateLimitException,
    BeehiivBadRequestException,
    BeehiivNotFoundException,
    BeehiivUnauthorizedException,
    BeehiivForbiddenException,
    BeehiivServerErrorException,
)
from .resources.automations import AutomationsResource
from .resources.publications import PublicationsResource
from .resources.subscriptions import SubscriptionsResource
from .resources.posts import PostsResource
from .resources.custom_fields import CustomFieldsResource
from .resources.segments import SegmentsResource
from .resources.tiers import TiersResource


class BeehiivClient:
    BASE_URL = "https://api.beehiiv.com/v2/"

    def __init__(self, api_key: str, timeout: int = 30):
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        # Initialize resource handlers
        self.publications = PublicationsResource(self)
        self.automations = AutomationsResource(self)
        self.subscriptions = SubscriptionsResource(self)
        self.posts = PostsResource(self)
        self.custom_fields = CustomFieldsResource(self)
        self.segments = SegmentsResource(self)
        self.tiers = TiersResource(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint.lstrip('/')}"

        try:
            response = self._session.request(
                method, url, params=params, json=json_data, timeout=self.timeout
            )
            response.raise_for_status() # Raises HTTPError for 4xx/5xx client/server errors
            if response.status_code == 204: # No Content
                return {"status": "success", "message": "Operation successful, no content returned."} # Provide a consistent return structure
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            try:
                error_data = e.response.json()
            except requests.exceptions.JSONDecodeError:
                error_data = {"error": e.response.text or "No error details provided."}

            error_message = f"API request to {url} failed with status {status_code}"
            # Try to get more specific error messages from Beehiiv's response
            if isinstance(error_data, dict):
                if 'message' in error_data:
                    error_message += f": {error_data['message']}"
                elif 'error' in error_data and isinstance(error_data['error'], str):
                    error_message += f": {error_data['error']}"
                elif 'errors' in error_data and isinstance(error_data['errors'], list) and error_data['errors']:
                    # Handle cases where 'errors' is a list of error objects
                    first_error = error_data['errors'][0]
                    if isinstance(first_error, dict) and 'message' in first_error:
                        error_message += f": {first_error['message']}"
                    elif isinstance(first_error, str):
                         error_message += f": {first_error}"


            if status_code == 400:
                raise BeehiivBadRequestException(error_message, status_code, error_data) from e
            elif status_code == 401:
                raise BeehiivUnauthorizedException(error_message, status_code, error_data) from e
            elif status_code == 403:
                raise BeehiivForbiddenException(error_message, status_code, error_data) from e
            elif status_code == 404:
                raise BeehiivNotFoundException(error_message, status_code, error_data) from e
            elif status_code == 429:
                raise BeehiivRateLimitException(error_message, status_code, error_data) from e
            elif status_code >= 500:
                raise BeehiivServerErrorException(error_message, status_code, error_data) from e
            else:
                raise BeehiivAPIException(error_message, status_code, error_data) from e
        except requests.exceptions.RequestException as e: # Catch other network errors
            raise BeehiivAPIException(f"Network request to {url} failed: {e}") from e

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, json_data=json_data)

    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("PUT", endpoint, json_data=json_data)

    def patch(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("PATCH", endpoint, json_data=json_data)

    def delete(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Some DELETE requests might have a body, though rare. Default to None.
        return self._request("DELETE", endpoint, json_data=json_data)