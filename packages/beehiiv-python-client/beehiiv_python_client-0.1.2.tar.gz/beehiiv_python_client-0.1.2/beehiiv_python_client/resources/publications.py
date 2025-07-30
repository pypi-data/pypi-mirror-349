from typing import Optional, Dict, Any, List
from .base import BaseResource


class PublicationsResource(BaseResource):
    def list(
        self,
        expand: Optional[List[str]] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        direction: Optional[str] = None, # "asc" or "desc"
        order_by: Optional[str] = None, # "created" or "name"
    ) -> Dict[str, Any]:
        """
        Retrieve all publications associated with your API key.

        Args:
            expand: List of fields to expand (e.g., "stats").
            limit: Number of results to return (1-100, default 10).
            page: Page number for pagination.
            direction: Sort direction ("asc" or "desc").
            order_by: Field to sort by ("created" or "name").
        Returns:
            Dict: The API response.
        """
        raw_params = {
            "expand": expand,
            "limit": limit,
            "page": page,
            "direction": direction,
            "order_by": order_by,
        }
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get("publications", params=params)

    def get(
        self,
        publication_id: str,
        expand: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve a single publication.

        Args:
            publication_id: The prefixed ID of the publication object.
            expand: List of fields to expand.
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")
        raw_params = {"expand": expand}
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}", params=params)

    def get_referral_program(
        self,
        publication_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve details about the publication’s referral program.

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
        return self._client.get(f"publications/{publication_id}/referral_program", params=params)