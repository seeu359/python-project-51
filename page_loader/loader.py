import os
from page_loader.lib.downloader import make_request, download_resources
from page_loader.lib.url_handling import check_url, format_webpage_url

FOLDER_SUFFIX = '_files'
HTML_SUFFIX = '.html'


def download(url: str, path_to_save_directory: str = os.getcwd()) -> str:
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

    download_resources(
        url,
        path_to_save_directory,
        path_to_resources_folder,
        path_to_main_html,
        webpage_data.text,
    )
    return path_to_main_html


def _get_path_to_main_resources(url: str,
                                path_to_save_directory: str) \
        -> tuple[str, str]:

    _formatted_webpage_url = format_webpage_url(url)
    path_to_resources_folder = os.path.join(
        path_to_save_directory,
        _formatted_webpage_url) + FOLDER_SUFFIX
    path_to_main_html = os.path.join(path_to_save_directory,
                                     _formatted_webpage_url) + HTML_SUFFIX
    return path_to_resources_folder, path_to_main_html
