import argparse
import os
from page_loader.lib.dataclasses import ArgumentParser
from typing import Literal


def get_parser_args() -> [Literal['url'], Literal['-o'], Literal['-output']]:
    """
    Return cli arguments: link and output path
    :return: ArgumentParser[str, str]
    """
    arguments = ArgumentParser(url='url', save_directory_short='-o',
                               save_directory_long='--output')
    parser = argparse.ArgumentParser(description='The utility downloads the '
                                                 'page from the web and saves '
                                                 'its html form to the '
                                                 'specified path')
    parser.add_argument(arguments.url)
    parser.add_argument(arguments.save_directory_short,
                        arguments.save_directory_long,
                        help='Select the path to save the file',
                        default=os.getcwd())

    return parser.parse_args()
