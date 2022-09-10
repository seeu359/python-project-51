import requests
from bs4 import BeautifulSoup
import os
import pathlib
from page_loader import link_handling as lh
from page_loader import file_handling as fh


def get_link_data(link):
    return requests.get(link).text


def get_link_pic(link):
    return requests.get(link, stream=True)


def get_local_resources(file_data, download_folder, link,
                        data_parser=get_link_pic,
                        data_recorder=fh.record_image):
    handler = BeautifulSoup(file_data, 'html.parser')
    find_img = handler.find_all('img')
    for img in find_img:
        pic_link = img['src']
        _, extension = os.path.splitext(pic_link)
        if (extension == '.png' or extension == '.jpg') and \
                lh.domain_check(pic_link, link) is True:
            constructed_link = lh.make_picture_link(link, pic_link)
            request = data_parser(constructed_link)
            save_path = os.path.join(download_folder,
                                     lh.get_format_link(
                                            constructed_link)) + extension
            pure_path = pathlib.PurePath(download_folder).name
            img['src'] = os.path.join(pure_path, lh.get_format_link(
                constructed_link) + extension)
            data_recorder(save_path, request)
    file_data = handler.prettify()
    return file_data
