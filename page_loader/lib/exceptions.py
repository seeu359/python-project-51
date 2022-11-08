class MissingSchemaError(Exception):
    """The URL scheme (e.g. http or https) is missing."""
    pass


class HttpRequestError(Exception):
    pass


class PageNotAvailableError(Exception):
    pass


class DirectoryCreationError(Exception):
    pass


class InvalidUrl(Exception):
    pass


class ResourceDownloadError(Exception):
    pass


class FileRecordingError(Exception):
    pass
