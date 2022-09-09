import os
from page_loader import downloaders
from page_loader import file_handling as fh
from page_loader import link_handling as lh


FORMAT_FILE = '.html'
FOLDER_SUFFIX = '_files'


def download(link, save_path=os.getcwd()):
    converted_link = lh.get_format_link(link)
    file_path = os.path.join(save_path, converted_link) + FORMAT_FILE
    with open(file_path, 'w') as html_file:
        html_file.write(downloaders.get_link_data(link))
        make_folder = fh.make_dir(converted_link, save_path)
        file_data = downloaders.download_pictures(file_path, make_folder, link)
        html_file.write(file_data)
    return file_path
