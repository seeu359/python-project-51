import logging
from urllib.parse import urlparse
import furl
import re
import os
import pathlib
from page_loader.exceptions import MissingSchemaError

FORMAT_FILE = '.html'


class PathBuilder:

    def __init__(self, webpage_link):
        self.webpage_link = webpage_link
        self.parse_link = urlparse(webpage_link)
        self.link_body, self.extension = os.path.splitext(webpage_link)
        self.processed_link = re.sub('http://|https://', '',
                                     self.link_body)

    def build_path_to_swap_in_html(self, save_folder) -> str:
        if not self.extension:
            self.extension = FORMAT_FILE
        replace_symbols_in_link = re.sub(r'[^a-zA-Z\d]', '-',
                                         self.processed_link)
        pure_path = pathlib.PurePath(save_folder).name
        return os.path.join(pure_path,
                            replace_symbols_in_link) + self.extension

    def build_link(self, file_path):
        parse_img_path = urlparse(file_path)
        if parse_img_path.scheme:
            return file_path
        link_body = f'{self.parse_link.scheme}://' \
                    f'{self.parse_link.netloc}'
        collected_link = furl.furl(link_body).add(path=file_path)
        return str(collected_link)

    def format_webpage_link(self):
        link_netloc = urlparse(self.webpage_link).netloc
        format_link = re.sub(r'[^a-zA-Z\d]', '-', link_netloc)
        return format_link

    def check_link(self):
        if not self.parse_link.scheme:
            logging.error(f'Missing scheme! Link - {self.webpage_link}')
            raise MissingSchemaError
