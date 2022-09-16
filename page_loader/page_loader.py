import os
from page_loader.downloaders import Downloaders
import requests


def download(link, save_path=os.getcwd()):
    data = requests.get(link).text
    main_obj = Downloaders(link, save_path, data)
    main_obj.download_all()
    return main_obj.main_file_path
