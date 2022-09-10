import os
from page_loader import downloaders
from page_loader import file_handling as fh
from page_loader import link_handling as lh


FORMAT_FILE = '.html'
FOLDER_SUFFIX = '_files'


def download(link, save_path=os.getcwd()):
    converted_link = lh.get_format_link(link)
    file_path = os.path.join(save_path, converted_link) + FORMAT_FILE
    make_folder = fh.make_dir(converted_link, save_path)
    link_data = downloaders.get_link_data(link)
    file_data = downloaders.get_local_resources(link_data, make_folder,
                                                link)
    with open(file_path, 'w') as html_file:
        html_file.write(file_data)
    return file_path
