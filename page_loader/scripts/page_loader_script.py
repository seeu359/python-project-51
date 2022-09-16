#!/usr/bin/env python
import logging

from page_loader.page_loader import download
from page_loader.cli import get_parser_args


def main():
    args = get_parser_args()
    logging.basicConfig(level=logging.INFO)
    logging.info('App started')
    print(download(args.link, args.output))


if __name__ == '__main__':
    main()
