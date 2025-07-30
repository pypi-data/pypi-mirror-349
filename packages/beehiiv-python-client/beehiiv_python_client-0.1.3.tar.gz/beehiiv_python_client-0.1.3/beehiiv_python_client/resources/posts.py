from typing import Optional, Dict, Any, List
from .base import BaseResource


class PostsResource(BaseResource):
    def create(
        self,
        publication_id: str,
        title: str,
        body_content: Optional[str] = None, # Raw HTML
        blocks: Optional[List[Dict[str, Any]]] = None, # Block editor content
        subtitle: Optional[str] = None,
        post_template_id: Optional[str] = None,
        status: Optional[str] = None, # "draft", "confirmed"
        scheduled_at: Optional[str] = None, # ISO 8601 datetime string
        custom_link_tracking_enabled: Optional[bool] = None,
        email_capture_type_override: Optional[str] = None, # "none", "gated", "popup"
        override_scheduled_at: Optional[str] = None, # ISO 8601 datetime string
        social_share: Optional[str] = None, # "comments_and_likes_only", "with_comments_and_likes", "top", "none"
        thumbnail_image_url: Optional[str] = None,
        recipients: Optional[Dict[str, Any]] = None,
        email_settings: Optional[Dict[str, Any]] = None,
        web_settings: Optional[Dict[str, Any]] = None,
        seo_settings: Optional[Dict[str, Any]] = None,
        content_tags: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        custom_fields: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a post for a specific publication. (Beta feature)

        Args:
            publication_id: The prefixed ID of the publication.
            title: The title of the post.
            body_content: Raw HTML content (alternative to blocks).
            blocks: List of block objects for the post content.
            subtitle: The subtitle of the post.
            # ... (add other args from API docs)
        Returns:
            Dict: The API response.
        """
        if not publication_id or not title:
            raise ValueError("publication_id and title are required.")
        if not body_content and not blocks:
            raise ValueError("Either body_content (HTML) or blocks must be provided.")
        if body_content and blocks:
            raise ValueError("Provide either body_content (HTML) or blocks, not both.")

        payload = self._build_params({
            "title": title,
            "body_content": body_content,
            "blocks": blocks,
            "subtitle": subtitle,
            "post_template_id": post_template_id,
            "status": status,
            "scheduled_at": scheduled_at,
            "custom_link_tracking_enabled": custom_link_tracking_enabled,
            "email_capture_type_override": email_capture_type_override,
            "override_scheduled_at": override_scheduled_at,
            "social_share": social_share,
            "thumbnail_image_url": thumbnail_image_url,
            "recipients": recipients,
            "email_settings": email_settings,
            "web_settings": web_settings,
            "seo_settings": seo_settings,
            "content_tags": content_tags,
            "headers": headers,
            "custom_fields": custom_fields
        })
        return self._client.post(f"publications/{publication_id}/posts", json_data=payload)

    def list(
        self,
        publication_id: str,
        expand: Optional[List[str]] = None,
        audience: Optional[str] = None, # "free", "premium", "all"
        platform: Optional[str] = None, # "web", "email", "both", "all"
        status: Optional[str] = None, # "draft", "confirmed", "archived", "all"
        content_tags: Optional[List[str]] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        order_by: Optional[str] = None, # "created", "publish_date", "displayed_date"
        direction: Optional[str] = None, # "asc", "desc"
        hidden_from_feed: Optional[str] = None, # "all", "true", "false"
    ) -> Dict[str, Any]:
        """
        Retrieve all posts belonging to a specific publication.

        Args:
            publication_id: The prefixed ID of the publication.
            expand: List of fields to expand (e.g., "stats", "free_web_content").
            audience: Filter by audience.
            # ... (add other args from API docs)
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")

        raw_params = {
            "expand": expand,
            "audience": audience,
            "platform": platform,
            "status": status,
            "content_tags": content_tags, # Will be formatted by _format_list_params
            "limit": limit,
            "page": page,
            "order_by": order_by,
            "direction": direction,
            "hidden_from_feed": hidden_from_feed,
        }
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/posts", params=params)

    def get_aggregate_stats(
        self,
        publication_id: str,
        audience: Optional[str] = None,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        content_tags: Optional[List[str]] = None,
        hidden_from_feed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve aggregate stats for all posts.

        Args:
            publication_id: The prefixed ID of the publication.
            # ... (add other query args from API docs)
        Returns:
            Dict: The API response.
        """
        if not publication_id:
            raise ValueError("publication_id is required.")

        raw_params = {
            "audience": audience,
            "platform": platform,
            "status": status,
            "content_tags": content_tags, # Will be formatted
            "hidden_from_feed": hidden_from_feed,
        }
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/posts/aggregate_stats", params=params)

    def get(
        self,
        publication_id: str,
        post_id: str,
        expand: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a single Post.

        Args:
            publication_id: The prefixed ID of the publication.
            post_id: The prefixed ID of the post.
            expand: List of fields to expand.
        Returns:
            Dict: The API response.
        """
        if not publication_id or not post_id:
            raise ValueError("publication_id and post_id are required.")
        raw_params = {"expand": expand}
        params = self._format_list_params(self._build_params(raw_params))
        return self._client.get(f"publications/{publication_id}/posts/{post_id}", params=params)

    def delete(self, publication_id: str, post_id: str) -> Dict[str, Any]:
        """
        Delete or Archive a post.

        Args:
            publication_id: The prefixed ID of the publication.
            post_id: The prefixed ID of the post.
        Returns:
            Dict: The API response (empty for 204 No Content).
        """
        if not publication_id or not post_id:
            raise ValueError("publication_id and post_id are required.")
        return self._client.delete(f"publications/{publication_id}/posts/{post_id}")

    # Note: Update Post (PUT/PATCH) is not explicitly listed in the provided docs,
    # but if it exists, it would be similar to create or other update methods.