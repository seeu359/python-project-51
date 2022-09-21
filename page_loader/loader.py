import logging
import os
from page_loader.downloaders import Downloaders
import requests


class PageNotAvailable(Exception):
    pass


def download(link, save_path=os.getcwd()):
    data = requests.get(link)
    status_code = data.status_code
    if status_code == 404:
        logging.error(f'Status code is not 200. Page {link} not available')
        raise PageNotAvailable
    main_obj = Downloaders(link, save_path, data.text)
    main_obj.download_all()
    return main_obj.main_file_path
