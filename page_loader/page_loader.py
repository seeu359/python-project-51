import os
from page_loader.downloaders import Downloaders


def download(link, save_path=os.getcwd()):
    main_obj = Downloaders(link, save_path)
    main_obj.download_all()
    return main_obj.main_file_path
