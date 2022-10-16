import os
import requests
from requests.exceptions import ConnectionError
from .log_config import logger
from typing import Literal, Callable
from page_loader.core.downloaders import Downloaders
from page_loader.core.link_handling import PathBuilder
from page_loader.core.dataclasses import DownloadInformation, FileSuffixes
from page_loader.exceptions import PageNotAvailableError, \
    DirectoryCreationError


def download(webpage_link: str, path_to_save_directory=os.getcwd()) -> str:
    PathBuilder(webpage_link).check_link()
    webpage_data = _make_request_by_link(webpage_link)
    path_to_main_html = _give_data_to_make_paths(
        FileSuffixes.HTML_FILE_SUFFIX, path_to_save_directory,
        webpage_link)
    path_to_resources_directory = _give_data_to_make_paths(
        FileSuffixes.FOLDER_SUFFIX, path_to_save_directory, webpage_link)
    _make_dir(path_to_resources_directory)
    download_information = DownloadInformation(
        webpage_link=webpage_link,
        path_to_save_directory=path_to_save_directory,
        webpage_data=webpage_data,
        path_to_resources_directory=path_to_resources_directory,
        path_to_main_html=path_to_main_html)
    main_obj = Downloaders(download_information)
    main_obj.download_all()
    return main_obj.path_to_main_html


def _make_request_by_link(link: str) -> str:
    try:
        request_by_link = requests.get(link)
    except ConnectionError as e:
        logger.error(f'Connection error! Error {e}')
        raise PageNotAvailableError
    request_status_code = request_by_link.status_code
    if request_status_code in (404, 500):
        logger.error(f'Page not Available error. Status code is '
                     f'{request_status_code}')
        raise PageNotAvailableError
    webpage_data = request_by_link.text
    return webpage_data


def _make_dir(path: str):
    try:
        os.mkdir(path)
    except PermissionError as e:
        logger.error(f'Can not create directory. Permission denied!'
                     f'Error: {e}')
        raise DirectoryCreationError
    except FileExistsError as e:
        logger.error(f'The directory already exists. Error: {e}')
        raise DirectoryCreationError
    except FileNotFoundError as e:
        logger.error(f'No such directory. Error: {e}')
        raise DirectoryCreationError


def _get_path_to_main_files(function: Callable) -> Callable:
    def wrapper(suffix: str,
                path_to_save_directory: str,
                webpage_link: str) -> str:

        suffix, path_to_save_directory, webpage_link = \
            function(suffix, path_to_save_directory, webpage_link)
        format_webpage_link = PathBuilder(
            webpage_link).format_webpage_link()
        path_to_main_file = os.path.join(path_to_save_directory,
                                         format_webpage_link) + suffix
        return path_to_main_file
    return wrapper


@_get_path_to_main_files
def _give_data_to_make_paths(suffix: Literal[FileSuffixes.FOLDER_SUFFIX,
                                             FileSuffixes.HTML_FILE_SUFFIX],
                             path_to_save_directory: str,
                             webpage_link: str) -> [Literal['_files',
                                                            '.html'],
                                                    str, str]:
    suffix_value = suffix.value
    return suffix_value, path_to_save_directory, webpage_link
