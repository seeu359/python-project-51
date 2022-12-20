#!/usr/bin/env python
import sys
from page_loader.loader import download
from page_loader.lib.cli import get_parser_args
from page_loader.lib import exception_messages as em


def main():
    args = get_parser_args()
    try:
        print(download(args.url, args.output))
        print(em.DOWNLOAD_SUCCESS)
        sys.exit(0)
    except Exception as e:
        print(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
