class MissingSchemaError(Exception):
    """The URL scheme (e.g. http or https) is missing."""
    pass


class PageNotAvailableError(Exception):
    pass


class DirectoryCreationError(Exception):
    pass


class ImageDownloadingError(Exception):
    pass


class TextDataDownloadingError(Exception):
    pass


class PermissionDenied(Exception):
    pass
