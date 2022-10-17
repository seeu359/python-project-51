import furl
import re
import os
import pathlib
from page_loader.log_config import logger
from urllib.parse import urlparse, urljoin
from page_loader.exceptions import MissingSchemaError
from page_loader.core.dataclasses import ExceptionLogMessage


FORMAT_FILE = '.html'


class PathHandler:
    """A class for handling file paths and local page resources,
    formatting links."""
    def __init__(self, webpage_link: str):
        self.webpage_link = webpage_link
        self.parse_link = urlparse(webpage_link)
        self.link_body, self.extension = os.path.splitext(webpage_link)
        self.processed_link = re.sub('http://|https://', '',
                                     self.link_body)

    def build_path_to_swap_in_html(self, save_folder: str) -> str:
        if not self.extension:
            self.extension = FORMAT_FILE
        replace_symbols_in_link = self.replace_dash(self.processed_link)
        pure_path = pathlib.PurePath(save_folder).name
        return os.path.join(pure_path,
                            replace_symbols_in_link) + self.extension

    def build_resource_link(self, file_path: str) -> str:
        """Build resource link for download"""
        parse_img_path = urlparse(file_path)
        if parse_img_path.scheme:
            return file_path
        link_body = f'{self.parse_link.scheme}://' \
                    f'{self.parse_link.netloc}'
        collected_link = furl.furl(link_body).add(path=file_path)
        return str(collected_link)

    def format_webpage_link(self) -> str:
        link_path = urlparse(self.webpage_link).path
        constructed_link = urljoin(self.webpage_link, link_path)
        replace_scheme = re.sub('http://|https://', '', constructed_link)
        format_link = self.replace_dash(replace_scheme)
        return format_link

    @staticmethod
    def replace_dash(link: str) -> str:
        """
        Delete dash from link
        :param link: str
        :return: str
        """
        format_link = re.sub(r'[^a-zA-Z\d]', '-', link)
        return format_link

    def check_link(self) -> None:
        """
        Check link scheme. If there's no scheme in link - missing scheme error
        raise
        :return: None
        """
        if not self.parse_link.scheme:
            logger.error(f'{ExceptionLogMessage.MISSING_SCHEMA.value}'
                         f'{self.webpage_link}')
            raise MissingSchemaError
