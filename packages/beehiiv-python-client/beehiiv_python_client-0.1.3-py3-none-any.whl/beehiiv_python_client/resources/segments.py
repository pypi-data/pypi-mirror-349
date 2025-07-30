from typing import Optional, Dict, Any, List
from .base import BaseResource


class SegmentsResource(BaseResource):
    def list(
        self,
        publication_id: str,
        type: Optional[str] = None, # "dynamic", "static", "manual", "all"
        status: Optional[str] = None, # "pending", "processing", "completed", "failed", "all"
        limit: Optional[int] = None,
        page: Optional[int] = None,
        order_by: Optional[str] = None, # "created", "last_calculated"
        direction: Optional[str] = None, # "asc", "desc"
        expand: Optional[List[str]] = None, # ["stats"]
    ) -> Dict[str, Any]:
        """
        Retrieve information about all segments.

        Args:
            publication_id: The prefixed ID of the publication.
            # ... (add other query args from API docs)
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")

        raw_params = {
            "type": type,
            "status": status,
            "limit": limit,
            "page": page,
            "order_by": order_by,
            "direction": direction,
            "expand": expand, # Will be formatted
        }
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/segments", params=params)

    def get(
        self,
        publication_id: str,
        segment_id: str,
        expand: Optional[List[str]] = None, # ["stats"]
    ) -> Dict[str, Any]:
        """
        Retrieve information about a specific segment.

        Args:
            publication_id: The prefixed ID of the publication.
            segment_id: The prefixed ID of the segment.
            expand: List of fields to expand.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not segment_id:
            raise ValueError("publication_id and segment_id are required.")
        raw_params = {"expand": expand}
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/segments/{segment_id}", params=params)

    def recalculate(self, publication_id: str, segment_id: str) -> Dict[str, Any]:
        """
        Recalculates a specific segment.

        Args:
            publication_id: The prefixed ID of the publication.
            segment_id: The prefixed ID of the segment.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not segment_id:
            raise ValueError("publication_id and segment_id are required.")
        return self._client.put(f"publications/{publication_id}/segments/{segment_id}/recalculate")

    def list_subscribers(
        self,
        publication_id: str,
        segment_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List the Subscriber Ids from the most recent calculation of a specific segment.

        Args:
            publication_id: The prefixed ID of the publication.
            segment_id: The prefixed ID of the segment.
            limit: Number of results to return.
            page: Page number for pagination.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not segment_id:
            raise ValueError("publication_id and segment_id are required.")
        params = self._build_params({"limit": limit, "page": page})
        return self._client.get(f"publications/{publication_id}/segments/{segment_id}/results", params=params)

    def delete(self, publication_id: str, segment_id: str) -> Dict[str, Any]:
        """
        Delete a segment.

        Args:
            publication_id: The prefixed ID of the publication.
            segment_id: The prefixed ID of the segment.
        Returns:
            Dict: The API response (empty for 204 No Content).
        """
        if not publication_id or not segment_id:
            raise ValueError("publication_id and segment_id are required.")
        return self._client.delete(f"publications/{publication_id}/segments/{segment_id}")

    # Note: Create Segment is not in the provided API docs snippet.
    # If it exists, it would be implemented here.