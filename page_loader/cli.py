import argparse
import os


def get_parser_args():
    parser = argparse.ArgumentParser(description='The utility downloads the '
                                                 'page from the web and saves '
                                                 'its html form to the '
                                                 'specified path')
    parser.add_argument('link')
    parser.add_argument('-o', '--output',
                        help='Select the path to save the file',
                        default=os.getcwd())

    return parser.parse_args()
