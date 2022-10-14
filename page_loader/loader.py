import logging
import os
from page_loader.downloaders import Downloaders
from page_loader.link_handling import PathBuilder
import requests
from page_loader.dataclasses import DownloadInformation
from page_loader.exceptions import PageNotAvailableError


def download(link: str, path_to_save_directory=os.getcwd()) -> str:
    PathBuilder(link).check_link()
    download_info = DownloadInformation(
        link=link, path_to_save_directory=path_to_save_directory)
    webpage_data = _make_request_by_link(link)
    main_obj = Downloaders(download_info, webpage_data)
    main_obj.download_all()
    return main_obj.main_file_path


def _make_request_by_link(link: str) -> str:
    request_by_link = requests.get(link)
    request_status_code = request_by_link.status_code
    if request_status_code in (404, 500):
        logging.error(f'Page not Available error. Status code is '
                      f'{request_status_code}')
        raise PageNotAvailableError
    webpage_data = request_by_link.text
    return webpage_data
