import os
import requests
from requests.exceptions import ConnectionError, InvalidSchema
from .log_config import logger
from typing import Literal, Callable
from page_loader.core.downloaders import Downloaders
from page_loader.core.link_handling import PathHandler
from page_loader.core.dataclasses import DownloadInformation, FileSuffixes, \
    Webpage, ExceptionLogMessage
from page_loader.exceptions import PageNotAvailableError, \
    DirectoryCreationError


def download(webpage_link: str, path_to_save_directory=os.getcwd()) -> str:
    """
    Main func of cli-utility. Runs in the main script. Returns the path to the
    main html file and prints it to the console.
    :param webpage_link: str
    :param path_to_save_directory: str
    :return: str
    """
    PathHandler(webpage_link).check_link()
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
        path_to_resources_directory=path_to_resources_directory,
        path_to_main_html=path_to_main_html)
    main_obj = Downloaders(download_information, webpage_data)
    main_obj.download_all()
    return main_obj.download_info.path_to_main_html


def _make_request_by_link(link: str) -> Webpage:
    try:
        request_by_link = requests.get(link)
    except ConnectionError as e:
        logger.error(f'{ExceptionLogMessage.CONNECTION_ERROR.value}'
                     f'{e}')
        raise PageNotAvailableError
    except InvalidSchema as e:
        logger.error(f'{ExceptionLogMessage.CONNECTION_ERROR.value}'
                     f'{e}')
        raise PageNotAvailableError
    request_status_code = request_by_link.status_code
    if request_status_code in (404, 500):
        logger.error(f'{ExceptionLogMessage.PAGE_NOT_AVAILABLE.value}'
                     f'{request_status_code}')
        raise PageNotAvailableError
    webpage_data = Webpage(webpage=request_by_link.text)
    return webpage_data


def _make_dir(path: str) -> None:
    try:
        os.mkdir(path)
    except PermissionError as e:
        logger.error(f'{ExceptionLogMessage.PERMISSION_DENIED.value}{e}')
        raise DirectoryCreationError
    except FileExistsError as e:
        logger.error(f'{ExceptionLogMessage.FILE_EXIST_ERROR.value}{e}')
        raise DirectoryCreationError
    except FileNotFoundError as e:
        logger.error(f'{ExceptionLogMessage.FILE_NOT_FOUND.value}{e}')
        raise DirectoryCreationError


def _get_path_to_main_files(function: Callable) -> Callable:
    def wrapper(suffix: str,
                path_to_save_directory: str,
                webpage_link: str) -> str:

        suffix, path_to_save_directory, webpage_link = \
            function(suffix, path_to_save_directory, webpage_link)
        format_webpage_link = PathHandler(
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
