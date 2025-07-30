from typing import Optional, Dict, Any, List
from .base import BaseResource


class CustomFieldsResource(BaseResource):
    def create(
        self,
        publication_id: str,
        kind: str,
        display: str,
    ) -> Dict[str, Any]:
        """
        Create a custom field on a publication.

        Args:
            publication_id: The prefixed ID of the publication object.
            kind: The type of value being stored (e.g., "string", "number", "date", "boolean", "url", "enum_single", "enum_multiple").
            display: The display name of the custom field.
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")
        payload = {"kind": kind, "display": display}
        return self._client.post(f"publications/{publication_id}/custom_fields", json_data=payload)

    def list(
        self,
        publication_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all custom fields on a publication.

        Args:
            publication_id: The prefixed ID of the publication object.
            limit: Number of results to return (1-100, default 10).
            page: Page number for pagination.
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")
        params = self._build_params({"limit": limit, "page": page})
        return self._client.get(f"publications/{publication_id}/custom_fields", params=params)

    def get(self, publication_id: str, custom_field_id: str) -> Dict[str, Any]:
        """
        View a specific custom field on a publication.

        Args:
            publication_id: The prefixed ID of the publication object.
            custom_field_id: The ID of the Custom Field object.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not custom_field_id:
            raise ValueError("publication_id and custom_field_id are required.")
        return self._client.get(f"publications/{publication_id}/custom_fields/{custom_field_id}")

    def update(
        self,
        publication_id: str,
        custom_field_id: str,
        display: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a custom field on a publication.
        Note: API docs show PUT and PATCH. Using PATCH for partial updates.

        Args:
            publication_id: The prefixed ID of the publication object.
            custom_field_id: The ID of the Custom Field object.
            display: The new display name for the custom field.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not custom_field_id:
            raise ValueError("publication_id and custom_field_id are required.")
        payload = self._build_params({"display": display})
        if not payload:
             raise ValueError("At least one field (display) must be provided for update.")
        return self._client.patch(f"publications/{publication_id}/custom_fields/{custom_field_id}", json_data=payload)

    def delete(self, publication_id: str, custom_field_id: str) -> Dict[str, Any]:
        """
        Delete a custom field from a publication.

        Args:
            publication_id: The prefixed ID of the publication object.
            custom_field_id: The ID of the Custom Field object.
        Returns:
            Dict: The API response (empty for 204 No Content).
        """
        if not publication_id or not custom_field_id:
            raise ValueError("publication_id and custom_field_id are required.")
        return self._client.delete(f"publications/{publication_id}/custom_fields/{custom_field_id}")