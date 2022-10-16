#!/usr/bin/env python
import sys
from page_loader.log_config import logger
from page_loader.loader import download
from page_loader.cli import get_parser_args
from page_loader.exceptions import MissingSchemaError, ImageDownloadingError, \
    TextDataDownloadingError, PageNotAvailableError


def main():
    logger.info('App started')
    args = get_parser_args()
    try:
        print(download(args.link, args.output))
        print('Page was downloaded!')
        sys.exit(0)
    except FileNotFoundError:
        print('Cannot create file in this path. The directory does not exist!')
        sys.exit(1)
    except PageNotAvailableError:
        print('Failed to load page!')
        sys.exit(1)
    except (ImageDownloadingError, TextDataDownloadingError):
        print('An error occurred while loading local resources!')
        sys.exit(1)
    except MissingSchemaError:
        print(f'There is no scheme in the page address. '
              f'Example link: "https://{args.link}"')
        sys.exit(1)


if __name__ == '__main__':
    main()
