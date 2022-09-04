#!/usr/bin/env python
from page_loader.page_loader import download
from page_loader.cli import get_parser_args


def main():
    args = get_parser_args()
    print(download(args.link, args.output))


if __name__ == '__main__':
    main()
