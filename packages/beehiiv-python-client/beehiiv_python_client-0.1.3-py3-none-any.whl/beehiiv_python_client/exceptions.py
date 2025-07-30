class BeehiivAPIException(Exception):
    """Base class for Beehiiv API exceptions."""
    def __init__(self, message, status_code=None, error_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.error_data = error_data
        self.message = message

    def __str__(self):
        return f"{self.message}"


class BeehiivBadRequestException(BeehiivAPIException):
    """HTTP 400 Bad Request."""
    pass


class BeehiivUnauthorizedException(BeehiivAPIException):
    """HTTP 401 Unauthorized."""
    pass


class BeehiivForbiddenException(BeehiivAPIException):
    """HTTP 403 Forbidden."""
    pass


class BeehiivNotFoundException(BeehiivAPIException):
    """HTTP 404 Not Found."""
    pass


class BeehiivRateLimitException(BeehiivAPIException):
    """HTTP 429 Too Many Requests."""
    pass


class BeehiivServerErrorException(BeehiivAPIException):
    """HTTP 5xx Server Error."""
    pass

# You can add more specific exceptions if needed based on API error codes/types