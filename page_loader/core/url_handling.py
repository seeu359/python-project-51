import furl
import re
import os
import pathlib
from page_loader.log_config import logger
from urllib.parse import urlparse, urljoin
from page_loader.exceptions import MissingSchemaError, InvalidUrl
from page_loader.core.dataclasses import ExceptionLogMessage


FORMAT_FILE = '.html'


class PathHandler:
    """A class for handling file paths and local page resources,
    formatting urls."""
    def __init__(self, url: str):
        self.webpage_url = url
        self.url_body, self.extension = os.path.splitext(url)
        self.processed_url = re.sub('http://|https://', '',
                                    self.url_body)
        try:
            self.parse_url = urlparse(url)
        except ValueError as e:
            logger.error(f'{ExceptionLogMessage.INVALID_URL.value}{url}. '
                         f'{e}')
            raise InvalidUrl

    def build_path_to_swap_in_html(self, save_folder: str) -> str:
        if not self.extension:
            self.extension = FORMAT_FILE
        replace_symbols_in_url = self.replace_dash(self.processed_url)
        pure_path = pathlib.PurePath(save_folder).name
        return os.path.join(pure_path,
                            replace_symbols_in_url) + self.extension

    def build_resource_url(self, file_path: str) -> str:
        """Build resource url for download"""
        parse_img_path = urlparse(file_path)
        if parse_img_path.scheme:
            return file_path
        url_body = f'{self.parse_url.scheme}://' \
                   f'{self.parse_url.netloc}'
        collected_url = furl.furl(url_body).add(path=file_path)
        return str(collected_url)

    def format_webpage_url(self) -> str:
        url_path = urlparse(self.webpage_url).path
        constructed_url = urljoin(self.webpage_url, url_path)
        replace_scheme = re.sub('http://|https://', '', constructed_url)
        format_url = self.replace_dash(replace_scheme)
        return format_url

    @staticmethod
    def replace_dash(url: str) -> str:
        """
        Delete dash from url
        :param url: str
        :return: str
        """
        format_url = re.sub(r'[^a-zA-Z\d]', '-', url)
        return format_url

    def check_url(self) -> None:
        """
        Check url scheme. If there's no scheme in url - missing scheme error
        raise
        :return: None
        """
        if not self.parse_url.scheme:
            logger.error(f'{ExceptionLogMessage.MISSING_SCHEMA.value}'
                         f'{self.webpage_url}')
            raise MissingSchemaError
