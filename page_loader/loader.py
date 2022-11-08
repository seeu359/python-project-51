import os
from page_loader.lib.logs.log_config import logger
from page_loader.lib import exception_messages as em
from page_loader.lib.downloader import Downloader, make_request
from page_loader.lib.url_handling import check_url, format_webpage_url
from page_loader.lib.exceptions import DirectoryCreationError

FOLDER_SUFFIX = '_files'
HTML_SUFFIX = '.html'


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
        logger.error(f'{em.PERMISSION_DENIED}{e}')
        raise DirectoryCreationError(em.USER_PERMISSION_DENIED) from e
    except FileExistsError as e:
        logger.error(f'{em.FILE_EXIST_ERROR}{e}')
        raise DirectoryCreationError(em.USER_DIRECTORY_EXIST) from e
    except FileNotFoundError as e:
        logger.error(f'{em.FILE_NOT_FOUND}{e}')
        raise DirectoryCreationError(em.DIRECTORY_CREATE_ERROR) from e


def _get_path_to_main_resources(url: str,
                                path_to_save_directory: str) \
        -> tuple[str, str]:

    _formated_webpage_url = format_webpage_url(url)
    path_to_resources_folder = os.path.join(
        path_to_save_directory,
        _formated_webpage_url) + FOLDER_SUFFIX
    path_to_main_html = os.path.join(path_to_save_directory,
                                     _formated_webpage_url) + HTML_SUFFIX
    return path_to_resources_folder, path_to_main_html
