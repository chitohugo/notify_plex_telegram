from plex_api_client.models.errors import GetRecentlyAddedLibraryBadRequest, GetRecentlyAddedLibraryUnauthorized, \
    GetThumbImageBadRequest, GetThumbImageUnauthorized, \
    GetServerListBadRequest, GetServerListUnauthorized, SDKError


class PlexSDKError(Exception):
    """Base class for all SDK-related exceptions."""
    pass


class BadRequestError(PlexSDKError):
    """Exception for bad requests."""
    pass


class UnauthorizedError(PlexSDKError):
    """Exception for authorization failures."""
    pass


class APIError(PlexSDKError):
    """General API error."""
    pass


def handle_exceptions(exception):
    exception_map = {
        GetRecentlyAddedLibraryBadRequest: BadRequestError,
        GetRecentlyAddedLibraryUnauthorized: UnauthorizedError,
        GetThumbImageBadRequest: BadRequestError,
        GetThumbImageUnauthorized: UnauthorizedError,
        GetServerListBadRequest: BadRequestError,
        GetServerListUnauthorized: UnauthorizedError,
        SDKError: APIError
    }

    exception_cls = exception_map.get(type(exception), PlexSDKError)
    raise exception_cls(f"{exception_cls.__name__}: {str(exception)}")
