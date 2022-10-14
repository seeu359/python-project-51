#!/usr/bin/env python
import logging
import sys
from page_loader.loader import download, PageNotAvailableError
from page_loader.link_handling import MissingSchemaError
from page_loader.cli import get_parser_args


logging.basicConfig(filename='/Users/a.cheremushkin/PythonProjects/'
                             'python-project-51/page_loader/logs.log',
                    level=logging.DEBUG)


def main():
    logging.info('App started')
    args = get_parser_args()
    try:
        print(download(args.link, args.output))
        print('Page was downloaded!')
        sys.exit(0)
    except PageNotAvailableError:
        print('Failed to load page!')
        sys.exit(1)
    except MissingSchemaError:
        print(f'There is no scheme in the page address. '
              f'Example link: "https://{args.link}"')
        sys.exit(1)


if __name__ == '__main__':
    main()
