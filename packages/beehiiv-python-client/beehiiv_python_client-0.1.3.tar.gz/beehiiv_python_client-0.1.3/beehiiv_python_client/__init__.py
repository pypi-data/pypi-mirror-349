from .client import BeehiivClient
from .exceptions import (
    BeehiivAPIException,
    BeehiivRateLimitException,
    BeehiivBadRequestException,
    BeehiivNotFoundException,
    BeehiivUnauthorizedException,
    BeehiivForbiddenException,
    BeehiivServerErrorException,
)

__version__ = "0.1.3" # Updated version

__all__ = [
    "BeehiivClient",
    "BeehiivAPIException",
    "BeehiivRateLimitException",
    "BeehiivBadRequestException",
    "BeehiivNotFoundException",
    "BeehiivUnauthorizedException",
    "BeehiivForbiddenException",
    "BeehiivServerErrorException",
]