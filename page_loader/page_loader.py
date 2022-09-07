import furl
import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pathlib

FORMAT_FILE = '.html'
FOLDER_SUFFIX = '_files'


def make_picture_link(page_link, picture_link):
    picture_link_pars = urlparse(picture_link)
    if picture_link_pars.scheme:
        return picture_link
    else:
        build_link = furl.furl(page_link).add(path=picture_link)
        return str(build_link)



def get_format_link(link):
    parse_link = urlparse(link)
    link_without_scheme = ''.join(parse_link[1:])
    template = re.findall(r'[\da-zA-Z-.]+\.[a-zAZ]+/[@\w/-]+\.\w+',
                          link_without_scheme)
    not_format_link = link_without_scheme[0:-1] if link.endswith('/') else \
        link_without_scheme

    if len(template) == 0:
        format_link = re.sub(r'[^a-zA-Z\d]', '-', not_format_link)
        return format_link

    else:
        check_extension = os.path.splitext(not_format_link)
        format_link = re.sub(r'[^a-zA-Z\d]', '-', check_extension[0])
        return format_link


def get_link_data(link):
    return requests.get(link).text


def make_dir(link, save_path):
    path_to_folder = os.path.join(save_path, link) + FOLDER_SUFFIX
    if os.path.exists(path_to_folder):
        return path_to_folder
    os.mkdir(path_to_folder)
    return path_to_folder


def download_pictures(webpage_path, download_folder, link):
    with open(webpage_path) as file:
        html_file = file.read()
    handler = BeautifulSoup(html_file, 'html.parser')
    find_img = handler.find_all('img')
    for img in find_img:
        pic_link = img['src']
        _, extension = os.path.splitext(pic_link)
        if extension == '.png' or extension == '.jpg':
            constructed_link = make_picture_link(link, pic_link)
            request = requests.get(constructed_link, stream=True)
            path_to_save = os.path.join(download_folder,
                                        get_format_link(
                                            constructed_link)) + extension
            pure_path = pathlib.PurePath(download_folder).name
            img['src'] = os.path.join(pure_path, get_format_link(
                constructed_link) + extension)
            with open(path_to_save, 'wb') as picture:
                for chunk in request.iter_content(chunk_size=1000):
                    picture.write(chunk)
    file_data = handler.prettify()
    return file_data


def download(link, save_path=os.getcwd()):
    converted_link = get_format_link(link)
    file_path = os.path.join(save_path, converted_link) + FORMAT_FILE
    with open(file_path, 'w') as html_file:
        html_file.write(get_link_data(link))
        make_folder = make_dir(converted_link, save_path)
        file_data = download_pictures(file_path, make_folder, link)
        html_file.write(file_data)
    return file_path
