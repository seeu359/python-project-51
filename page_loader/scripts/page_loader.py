#!/usr/bin/env python
import logging
import sys
from page_loader.loader import download
from page_loader.cli import get_parser_args
from page_loader.exceptions import MissingSchemaError, ImageDownloadingError, \
    TextDataDownloadingError, PageNotAvailableError


logging.basicConfig(format='%(levelname)s :: %(asctime)s :: %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filename='/Users/a.cheremushkin/PythonProjects/'
                             'python-project-51/page_loader/logs.log',
                    level=logging.DEBUG)


def main():
    logging.info('App started')
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
