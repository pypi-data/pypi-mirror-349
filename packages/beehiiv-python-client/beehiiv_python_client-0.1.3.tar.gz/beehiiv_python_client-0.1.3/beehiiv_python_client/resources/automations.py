from typing import Optional, Dict, Any, List
from .base import BaseResource


class AutomationsResource(BaseResource):
    def add_subscription_to_journey(
        self,
        publication_id: str,
        automation_id: str,
        email: Optional[str] = None,
        subscription_id: Optional[str] = None,
        double_opt_override: Optional[str] = None, # "on", "off", or None
    ) -> Dict[str, Any]:
        """
        Add an existing subscription to an automation flow.
        Requires the automation to have an active Add by API trigger.

        Args:
            publication_id: The prefixed ID of the publication object.
            automation_id: The prefixed ID of the automation object.
            email: The email address associated with the subscription.
            subscription_id: The prefixed ID of the subscription.
            double_opt_override: Override publication double-opt settings.
                                 Allowed values: "on", "off".
        Returns:
            Dict: The API response.
        """
        if not publication_id or not automation_id:
            raise ValueError("publication_id and automation_id are required.")
        if not email and not subscription_id:
            raise ValueError("Either email or subscription_id must be provided.")

        payload: Dict[str, Any] = {}
        if email:
            payload["email"] = email
        if subscription_id:
            payload["subscription_id"] = subscription_id
        if double_opt_override:
            payload["double_opt_override"] = double_opt_override

        endpoint = f"publications/{publication_id}/automations/{automation_id}/journeys"
        return self._client.post(endpoint, json_data=payload)

    def list_journeys(
        self,
        publication_id: str,
        automation_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of automation journeys for a specific automation.

        Args:
            publication_id: The prefixed ID of the publication object.
            automation_id: The prefixed ID of the automation object.
            limit: Limit the number of results (1-100, default 10).
            page: Page number for pagination.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not automation_id:
            raise ValueError("publication_id and automation_id are required.")

        params = self._build_params({"limit": limit, "page": page})
        endpoint = f"publications/{publication_id}/automations/{automation_id}/journeys"
        return self._client.get(endpoint, params=params)

    def get_journey(
        self,
        publication_id: str,
        automation_id: str,
        automation_journey_id: str,
    ) -> Dict[str, Any]:
        """
        Retrieve a single automation journey by ID.

        Args:
            publication_id: The prefixed ID of the publication object.
            automation_id: The prefixed ID of the automation object.
            automation_journey_id: The prefixed ID of the automation journey.
        Returns:
            Dict: The API response.
        """
        if not all([publication_id, automation_id, automation_journey_id]):
            raise ValueError("publication_id, automation_id, and automation_journey_id are required.")

        endpoint = f"publications/{publication_id}/automations/{automation_id}/journeys/{automation_journey_id}"
        return self._client.get(endpoint)

    def list_automations(
        self,
        publication_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of automations for a specific publication.

        Args:
            publication_id: The prefixed ID of the publication object.
            limit: Limit the number of results (1-100, default 10).
            page: Page number for pagination.
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")

        params = self._build_params({"limit": limit, "page": page})
        endpoint = f"publications/{publication_id}/automations"
        return self._client.get(endpoint, params=params)

    def get_automation(
        self,
        publication_id: str,
        automation_id: str,
    ) -> Dict[str, Any]:
        """
        Retrieve a single automation by ID.

        Args:
            publication_id: The prefixed ID of the publication object.
            automation_id: The prefixed ID of the automation object.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not automation_id:
            raise ValueError("publication_id and automation_id are required.")
        endpoint = f"publications/{publication_id}/automations/{automation_id}"
        return self._client.get(endpoint)