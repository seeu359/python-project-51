#!/usr/bin/env python
import sys
from page_loader.loader import download
from page_loader.lib.cli import get_parser_args
from page_loader.lib import exception_messages as em
from page_loader.lib.exceptions import MissingSchemaError,\
    PageNotAvailableError, DirectoryCreationError, InvalidUrl, \
    HttpRequestError, ResourceDownloadError, FileRecordingError


def main():
    args = get_parser_args()
    try:
        print(download(args.url, args.output))
        print(em.DOWNLOAD_SUCCESS)
        sys.exit(0)
    except DirectoryCreationError as e:
        print(str(e))
        sys.exit(1)
    except (HttpRequestError, PageNotAvailableError):
        print(em.FAILED_TO_LOAD)
        sys.exit(1)
    except ResourceDownloadError:
        sys.exit(1)
    except FileRecordingError as e:
        print(str(e))
        sys.exit(1)
    except MissingSchemaError:
        print(em.MISSING_SCHEME + args.url)
        sys.exit(1)
    except InvalidUrl:
        print(em.INVALID_URL)
        sys.exit(1)


if __name__ == '__main__':
    main()
