import requests
import logging
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import furl
import re

logging.basicConfig(level=logging.INFO)


def check_image_extension(path):
    _, extension = os.path.splitext(path)
    if extension == '.png' or extension == '.jpeg':
        return True
    return False


def domain_check(resource_link, web_page):
    picture_link_parse = urlparse(resource_link)
    web_page_parse = urlparse(web_page)
    if not picture_link_parse.scheme:
        return True
    else:
        return True if web_page_parse.netloc == picture_link_parse.netloc \
            else False


def image_recorder(path, data):
    with open(path, 'wb') as image:
        for chunk in data.iter_content(chunk_size=1000):
            image.write(chunk)


class Downloaders:

    img_tag = ('img', 'src')
    link_tag = ('link', 'href')
    script_tag = ('script', 'src')

    def __init__(self, link, save_folder):
        self.link = link
        self.save_folder = save_folder
        self.link_data = BeautifulSoup(self.get_link_data(), 'html.parser')

    def get_link_data(self):
        logging.info(f'request {self.link}')

        return requests.get(self.link).text

    @staticmethod
    def get_image_data(link):
        return requests.get(link, stream=True)

    def get_resources_lst(self, tag):
        tag_name, tag_attr = tag
        resources = self.link_data.find_all(tag_name, {tag_attr: True})
        resources_list = list()
        for res in resources:
            resources_list.append(res[tag_attr])
        return resources_list

    def download_image(self):
        link_list = self.get_resources_lst(self.img_tag)
        for img_path in link_list:
            if check_image_extension(img_path) and \
                    domain_check(img_path, self.link):
                link = PathBuilder(self.link).build_link(img_path)
                data = self.get_image_data(link)
                path = PathBuilder(link).make_save_path(self.save_folder)
                image_recorder(path, data)


class PathBuilder:

    def __init__(self, link):
        self.link = link

    def make_save_path(self, save_folder):
        body, extension = os.path.splitext(self.link)
        delete_scheme_in_link = re.sub('http://|https://', '', body)
        replace_symbols_in_link = re.sub(r'[^a-zA-Z\d]', '-',
                                         delete_scheme_in_link)
        return os.path.join(save_folder, replace_symbols_in_link) + extension

    def build_link(self, file_path):
        parse_img_path = urlparse(file_path)
        parse_webpage_link = urlparse(self.link)
        if parse_img_path.scheme:
            return file_path
        link_body = f'{parse_webpage_link.scheme}://' \
                    f'{parse_webpage_link.netloc}'
        collected_link = furl.furl(link_body).add(path=file_path)
        return str(collected_link)
