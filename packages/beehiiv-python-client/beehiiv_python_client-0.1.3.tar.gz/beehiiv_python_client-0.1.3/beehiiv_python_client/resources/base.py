from typing import TYPE_CHECKING, Optional, Dict, Any, List

if TYPE_CHECKING:
    from ..client import BeehiivClient # To avoid circular import


class BaseResource:
    def __init__(self, client: 'BeehiivClient'):
        self._client = client

    def _build_params(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Helper to filter out None values from params."""
        if params is None:
            return {}
        return {k: v for k, v in params.items() if v is not None}

    def _format_list_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Beehiiv API sometimes uses `param_name[]` for list query parameters.
        This method checks for list values and renames keys accordingly.
        """
        formatted_params = {}
        for key, value in params.items():
            if isinstance(value, list):
                # Ensure all list items are strings for query params
                formatted_params[f"{key}[]"] = [str(item) for item in value]
            else:
                formatted_params[key] = value
        return formatted_params