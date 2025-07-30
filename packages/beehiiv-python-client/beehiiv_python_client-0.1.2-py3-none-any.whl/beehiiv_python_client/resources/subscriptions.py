from typing import Optional, Dict, Any, List
from .base import BaseResource

class SubscriptionsResource(BaseResource):
    def create(
        self,
        publication_id: str,
        email: str,
        reactivate_existing: Optional[bool] = None,
        send_welcome_email: Optional[bool] = None,
        utm_source: Optional[str] = None,
        utm_medium: Optional[str] = None,
        utm_campaign: Optional[str] = None,
        referring_site: Optional[str] = None,
        referral_code: Optional[str] = None,
        custom_fields: Optional[List[Dict[str, str]]] = None, # [{"name": "X", "value": "Y"}]
        double_opt_override: Optional[str] = None, # "on", "off"
        tier: Optional[str] = None, # "free", "premium"
        premium_tier_ids: Optional[List[str]] = None,
        stripe_customer_id: Optional[str] = None,
        automation_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        if not publication_id or not email:
            raise ValueError("publication_id and email are required.")

        payload = self._build_params({
            "email": email,
            "reactivate_existing": reactivate_existing,
            "send_welcome_email": send_welcome_email,
            "utm_source": utm_source,
            "utm_medium": utm_medium,
            "utm_campaign": utm_campaign,
            "referring_site": referring_site,
            "referral_code": referral_code,
            "custom_fields": custom_fields,
            "double_opt_override": double_opt_override,
            "tier": tier,
            "premium_tier_ids": premium_tier_ids,
            "stripe_customer_id": stripe_customer_id,
            "automation_ids": automation_ids
        })
        return self._client.post(f"publications/{publication_id}/subscriptions", json_data=payload)

    def list(
        self,
        publication_id: str,
        # ... add all query parameters from API docs ...
        email: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        status: Optional[str] = None,
        tier: Optional[str] = None,
        expand: Optional[List[str]] = None,
        premium_tier_ids: Optional[List[str]] = None,
        # ... and so on
    ) -> Dict[str, Any]:
        if not publication_id:
            raise ValueError("publication_id is required.")

        raw_params = self._build_params({
            "email": email,
            "limit": limit,
            "page": page,
            "status": status,
            "tier": tier,
            "expand": expand,
            "premium_tier_ids": premium_tier_ids
            # ...
        })
        params = self._format_list_params(raw_params)
        return self._client.get(f"publications/{publication_id}/subscriptions", params=params)

    def get_by_id(
        self,
        publication_id: str,
        subscription_id: str,
        expand: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        if not publication_id or not subscription_id:
            raise ValueError("publication_id and subscription_id are required.")
        raw_params = {"expand": expand}
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/subscriptions/{subscription_id}", params=params)

    def get_by_email(
        self,
        publication_id: str,
        email: str, # Needs to be URL encoded by the requests library automatically
        expand: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        if not publication_id or not email:
            raise ValueError("publication_id and email are required.")
        raw_params = {"expand": expand}
        params = self._format_list_params(self._build_params(raw_params))
        # The requests library should handle URL encoding of the email in the path
        return self._client.get(f"publications/{publication_id}/subscriptions/by_email/{email}", params=params)

    def update(
        self,
        publication_id: str,
        subscription_id: str,
        tier: Optional[str] = None, # "free", "premium"
        stripe_customer_id: Optional[str] = None,
        unsubscribe: Optional[bool] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None,
        # Add other updatable fields
    ) -> Dict[str, Any]:
        if not publication_id or not subscription_id:
            raise ValueError("publication_id and subscription_id are required.")

        payload = self._build_params({
            "tier": tier,
            "stripe_customer_id": stripe_customer_id,
            "unsubscribe": unsubscribe,
            "custom_fields": custom_fields,
        })
        # Beehiiv API docs show PUT and PATCH for this. Let's default to PATCH for partial updates.
        return self._client.patch(f"publications/{publication_id}/subscriptions/{subscription_id}", json_data=payload)


    def delete(self, publication_id: str, subscription_id: str) -> Dict[str, Any]:
        if not publication_id or not subscription_id:
            raise ValueError("publication_id and subscription_id are required.")
        return self._client.delete(f"publications/{publication_id}/subscriptions/{subscription_id}")

    def add_tag(
        self,
        publication_id: str,
        subscription_id: str,
        tags: List[str],
    ) -> Dict[str, Any]:
        """
        Adds tags to a subscription.

        Args:
            publication_id: The prefixed ID of the publication.
            subscription_id: The prefixed ID of the subscription.
            tags: A list of tags to add.
        Returns:
            Dict: The API response with the updated subscription object.
        """
        if not publication_id or not subscription_id:
            raise ValueError("publication_id and subscription_id are required.")
        if not tags:
            raise ValueError("tags list cannot be empty.")

        payload = {"tags": tags}
        return self._client.post(f"publications/{publication_id}/subscriptions/{subscription_id}/tags", json_data=payload)

    def bulk_update_fields(
        self,
        publication_id: str,
        subscriptions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Bulk update multiple subscriptions fields, including status, custom fields, and tiers.
        Uses PATCH as per API docs (PUT is also available but PATCH is generally for partial updates).

        Args:
            publication_id: The prefixed ID of the publication.
            subscriptions: A list of subscription objects to update. Each object can contain:
                           "subscription_id": str (required)
                           "tier": str (optional - "free", "premium")
                           "stripe_customer_id": str (optional)
                           "unsubscribe": bool (optional)
                           "custom_fields": List[Dict[str, str]] (optional - [{"name": "X", "value": "Y"}])
        Returns:
            Dict: The API response, typically including a "subscription_update_id".
        """
        if not publication_id:
            raise ValueError("publication_id is required.")
        if not subscriptions:
            raise ValueError("subscriptions list cannot be empty.")
        for sub_data in subscriptions:
            if "subscription_id" not in sub_data:
                raise ValueError("Each item in subscriptions list must have a 'subscription_id'.")


        payload = {"subscriptions": subscriptions}
        return self._client.patch(f"publications/{publication_id}/subscriptions/bulk_actions", json_data=payload)

    def bulk_update_status(
        self,
        publication_id: str,
        subscription_ids: List[str],
        new_status: str,
    ) -> Dict[str, Any]:
        """
        Bulk update subscriptions' status.
        Uses PATCH as per API docs (PUT is also available).

        Args:
            publication_id: The prefixed ID of the publication.
            subscription_ids: A list of subscription IDs to be updated.
            new_status: The new status to set for the subscriptions (e.g., "active", "inactive", etc.).
        Returns:
            Dict: The API response. (The API docs for this endpoint don't show a response body for 200 OK,
                  but the PATCH/PUT bulk_actions does. Assuming this might return a status or update ID).
                  Let's assume it could return something or be a 204. The client handles 204.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")
        if not subscription_ids:
            raise ValueError("subscription_ids list cannot be empty.")
        if not new_status:
            raise ValueError("new_status cannot be empty.")

        payload = {"subscription_ids": subscription_ids, "new_status": new_status}
        # The doc shows PUT and PATCH for this endpoint. Let's use PATCH for consistency.
        # The endpoint is /subscriptions, not /subscriptions/bulk_actions
        return self._client.patch(f"publications/{publication_id}/subscriptions", json_data=payload)


    def list_subscription_updates(
        self,
        publication_id: str,
        # Add query params if available in full docs: limit, page, etc.
    ) -> Dict[str, Any]:
        """
        Returns a list of Subscription Update objects for a publication.

        Args:
            publication_id: The prefixed ID of the publication object.
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")
        return self._client.get(f"publications/{publication_id}/bulk_subscription_updates")


    def get_subscription_update(
        self,
        publication_id: str,
        update_id: str,
    ) -> Dict[str, Any]:
        """
        Returns a single Subscription Update object for a publication.

        Args:
            publication_id: The prefixed ID of the publication object.
            update_id: The ID of the Subscription Update object.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not update_id:
            raise ValueError("publication_id and update_id are required.")
        return self._client.get(f"publications/{publication_id}/bulk_subscription_updates/{update_id}")