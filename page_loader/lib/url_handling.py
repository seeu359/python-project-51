import furl
import re
import os
import pathlib
from page_loader.lib.logs.log_config import logger
from urllib.parse import urlparse, urljoin
from page_loader.lib.exceptions import MissingSchemaError, InvalidUrl
from page_loader.lib import exception_messages as em


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
            logger.error(f'{em.INVALID_URL}{url}. '
                         f'{e}')
            raise InvalidUrl(em.INVALID_URL)

    def build_path_to_swap_in_html(self, save_folder: str) -> str:
        if not self.extension:
            self.extension = FORMAT_FILE
        replace_symbols_in_url = replace_dash(self.processed_url)
        pure_path = pathlib.PurePath(save_folder).name
        return os.path.join(pure_path,
                            replace_symbols_in_url) + self.extension


def build_resource_url(url: str, file_path: str) -> str:
    """Build resource url for download"""
    parse_url = urlparse(url)
    parse_file_path = urlparse(file_path)
    if parse_file_path.scheme:
        return file_path
    url_body = f'{parse_url.scheme}://' \
               f'{parse_url.netloc}'
    collected_url = furl.furl(url_body).add(path=file_path)
    return str(collected_url)


def format_webpage_url(url: str) -> str:
    url_path = urlparse(url).path
    constructed_url = urljoin(url, url_path)
    replace_scheme = re.sub('http://|https://', '', constructed_url)
    format_url = replace_dash(replace_scheme)
    return format_url


def replace_dash(url: str) -> str:
    """
    Delete dash from url
    :param url: str
    :return: str
    """
    format_url = re.sub(r'[^a-zA-Z\d]', '-', url)
    return format_url


def check_url(url) -> None:
    """
    Check url scheme. If there's no scheme in url - missing scheme error
    raise
    :return: None
    """
    parse_url = urlparse(url)
    if not parse_url.scheme:
        logger.error(f'{em.MISSING_SCHEME}'
                     f'{url}')
        raise MissingSchemaError(em.MISSING_SCHEME)
