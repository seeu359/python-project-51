import os
from .log_config import logger
from page_loader.core.downloader import Downloader, make_request_by_url
from page_loader.core.url_handling import PathHandler
from page_loader.core.dataclasses import FileSuffixes, ExceptionLogMessage
from page_loader.exceptions import DirectoryCreationError, \
    PageNotAvailableError


def download(url: str, path_to_save_directory=os.getcwd()) -> str:
    """
    Main func of cli-utility. Runs in the main script. Returns the path to the
    main html file and prints it to the console.
    :param url: str
    :param path_to_save_directory: str
    :return: str
    """
    PathHandler(url).check_url()
    webpage_data = make_request_by_url(url,
                                       ExceptionLogMessage.PAGE_NOT_AVAILABLE,
                                       PageNotAvailableError)

    path_to_resources_folder, path_to_main_html = \
        _get_path_to_main_resources(FileSuffixes.FOLDER_SUFFIX,
                                    FileSuffixes.HTML_FILE_SUFFIX,
                                    path_to_save_directory, url)

    _make_dir(path_to_resources_folder)

    downloader = Downloader(url, path_to_save_directory,
                            path_to_resources_folder, path_to_main_html,
                            webpage_data.text)
    downloader.download_all()
    return downloader.path_to_main_html


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


def _get_path_to_main_resources(folder_suffix: FileSuffixes,
                                html_suffix: FileSuffixes,
                                path_to_save_directory: str,
                                url: str) -> tuple[str, str]:

    format_webpage_url = PathHandler(url).format_webpage_url()
    path_to_resources_folder = os.path.join(
        path_to_save_directory,
        format_webpage_url) + folder_suffix.value
    path_to_main_html = os.path.join(path_to_save_directory,
                                     format_webpage_url) + html_suffix.value
    return path_to_resources_folder, path_to_main_html
