#!/usr/bin/env python
import logging
import os
import sys

from page_loader.loader import download, PageNotAvailable
from page_loader.cli import get_parser_args


logging.basicConfig(filename=os.path.join(os.path.abspath(os.curdir),
                                          'page_loader/logs.log'),
                    level=logging.DEBUG)


def main():
    logging.info('App started')
    args = get_parser_args()
    try:
        print(download(args.link, args.output))
        sys.exit(0)
    except PageNotAvailable:
        print('Failed to load page (error 404)')
        sys.exit(1)


if __name__ == '__main__':
    main()
