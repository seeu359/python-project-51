import os
from .log_config import logger
from page_loader.core import exception_messages
from page_loader.core.downloader import Downloader, make_request
from page_loader.core.url_handling import check_url, format_webpage_url
from page_loader.exceptions import DirectoryCreationError


def download(url: str, path_to_save_directory=os.getcwd()) -> str:
    """
    Main func of cli-utility. Runs in the main script. Returns the path to the
    main html file and prints it to the console.
    :param url: str
    :param path_to_save_directory: str
    :return: str
    """
    check_url(url)
    webpage_data = make_request(url)

    path_to_resources_folder, path_to_main_html = \
        _get_path_to_main_resources(url, path_to_save_directory)

    _make_dir(path_to_resources_folder)

    downloader = Downloader(url, path_to_save_directory,
                            path_to_resources_folder, path_to_main_html,
                            webpage_data.text)
    downloader.download_all()
    return path_to_main_html


def _make_dir(path: str) -> None:
    try:
        os.mkdir(path)
    except PermissionError as e:
        logger.error(f'{exception_messages.PERMISSION_DENIED}{e}')
        raise DirectoryCreationError
    except FileExistsError as e:
        logger.error(f'{exception_messages.FILE_EXIST_ERROR}{e}')
        raise DirectoryCreationError
    except FileNotFoundError as e:
        logger.error(f'{exception_messages.FILE_NOT_FOUND}{e}')
        raise DirectoryCreationError


def _get_path_to_main_resources(url: str, path_to_save_directory: str,
                                folder_suffix='_files',
                                html_suffix='.html') -> tuple[str, str]:

    _format_webpage_url = format_webpage_url(url)
    path_to_resources_folder = os.path.join(
        path_to_save_directory,
        _format_webpage_url) + folder_suffix
    path_to_main_html = os.path.join(path_to_save_directory,
                                     _format_webpage_url) + html_suffix
    return path_to_resources_folder, path_to_main_html
