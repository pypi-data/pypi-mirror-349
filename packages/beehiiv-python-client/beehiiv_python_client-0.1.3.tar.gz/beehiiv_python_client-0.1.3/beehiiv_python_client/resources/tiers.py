from typing import Optional, Dict, Any, List
from .base import BaseResource


class TiersResource(BaseResource):
    def create(
        self,
        publication_id: str,
        name: str,
        description: Optional[str] = None,
        prices_attributes: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new tier for a publication.

        Args:
            publication_id: The prefixed ID of the publication.
            name: The name of the tier.
            description: Description of the tier.
            prices_attributes: List of price attributes for the tier.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not name:
            raise ValueError("publication_id and name are required.")

        payload = self._build_params({
            "name": name,
            "description": description,
            "prices_attributes": prices_attributes,
        })
        return self._client.post(f"publications/{publication_id}/tiers", json_data=payload)

    def list(
        self,
        publication_id: str,
        expand: Optional[List[str]] = None, # ["stats", "prices"]
        limit: Optional[int] = None,
        page: Optional[int] = None,
        direction: Optional[str] = None, # "asc", "desc"
    ) -> Dict[str, Any]:
        """
        Retrieve all tiers belonging to a specific publication.

        Args:
            publication_id: The prefixed ID of the publication.
            expand: List of fields to expand.
            limit: Number of results to return.
            page: Page number for pagination.
            direction: Sort direction.
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")

        raw_params = {
            "expand": expand, # Will be formatted
            "limit": limit,
            "page": page,
            "direction": direction,
        }
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/tiers", params=params)

    def get(
        self,
        publication_id: str,
        tier_id: str,
        expand: Optional[List[str]] = None, # ["stats", "prices"]
    ) -> Dict[str, Any]:
        """
        Retrieve a single tier.

        Args:
            publication_id: The prefixed ID of the publication.
            tier_id: The prefixed ID of the tier.
            expand: List of fields to expand.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not tier_id:
            raise ValueError("publication_id and tier_id are required.")
        raw_params = {"expand": expand}
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/tiers/{tier_id}", params=params)

    def update(
        self,
        publication_id: str,
        tier_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        prices_attributes: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing tier.
        Note: API docs show PUT and PATCH. Using PATCH for partial updates.

        Args:
            publication_id: The prefixed ID of the publication.
            tier_id: The prefixed ID of the tier.
            name: The new name of the tier.
            description: The new description of the tier.
            prices_attributes: List of price attributes to update/add/delete.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not tier_id:
            raise ValueError("publication_id and tier_id are required.")

        payload = self._build_params({
            "name": name,
            "description": description,
            "prices_attributes": prices_attributes,
        })
        if not payload:
            raise ValueError("At least one field must be provided for update.")
        return self._client.patch(f"publications/{publication_id}/tiers/{tier_id}", json_data=payload)

    # Note: Delete Tier is not in the provided API docs snippet.
    # If it exists, it would be implemented here.