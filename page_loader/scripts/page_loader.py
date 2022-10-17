#!/usr/bin/env python
import sys
from page_loader.loader import download
from page_loader.core.cli import get_parser_args
from page_loader.core.dataclasses import UserMessage
from page_loader.exceptions import MissingSchemaError, ImageDownloadingError, \
    TextDataDownloadingError, PageNotAvailableError, DirectoryCreationError


def main():
    args = get_parser_args()
    try:
        print(download(args.link, args.output))
        print(UserMessage.DOWNLOAD_SUCCESS.value)
        sys.exit(0)
    except DirectoryCreationError:
        print(UserMessage.DIRECTORY_CREATE_ERROR.value)
        sys.exit(1)
    except PageNotAvailableError:
        print(UserMessage.FAILED_TO_LOAD.value)
        sys.exit(1)
    except (ImageDownloadingError, TextDataDownloadingError):
        print(UserMessage.DATA_DOWNLOAD_ERROR.value)
        sys.exit(1)
    except MissingSchemaError:
        print(UserMessage.MISSING_SCHEME.value + args.link)
        sys.exit(1)


if __name__ == '__main__':
    main()
