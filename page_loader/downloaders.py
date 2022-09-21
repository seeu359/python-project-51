import sys

import requests
import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.file_handling import FileWorker
from page_loader.link_handling import PathBuilder

FOLDER_SUFFIX = '_files'
FORMAT_FILE = '.html'


class Downloaders:

    tags = {'img': ('img', 'src'),
            'link': ('link', 'href'),
            'script': ('script', 'src')}

    def __init__(self, link: str, save_path: str, data: str):
        self.link = link
        self.format_link = PathBuilder(link).format_link()
        self.data = BeautifulSoup(data, 'html.parser')
        self.save_path = save_path
        self.main_file_path = os.path.join(self.save_path,
                                           self.format_link) + FORMAT_FILE
        self.resource_folder = os.path.join(save_path,
                                            self.format_link) + FOLDER_SUFFIX

    @staticmethod
    def get_image_data(link: str) -> requests.models.Response:
        return requests.get(link, stream=True)

    @staticmethod
    def get_text_data(link: str) -> str:
        return requests.get(link).text

    def get_resources_lst(self, tag: str) -> list:
        tag_name, tag_attr = tag
        resources = self.data.find_all(tag_name, {tag_attr: True})
        return resources

    def download_resources(self, tag: str) -> None:
        resource_loader = self.get_image_data if tag == 'img' else \
            self.get_text_data
        _, tag_attr = self.tags[tag]
        resource_list = self.get_resources_lst(self.tags[tag])
        for res in resource_list:
            resource = res[tag_attr]
            if checker(tag, resource, self.link):
                link = PathBuilder(self.link).build_link(resource)
                resource_data = resource_loader(link)
                path = self.change_path_in_html(link, res, tag)
                self.record_resources(tag, path, resource_data)

    def change_path_in_html(self, link: str, resource: dict, tag: str) -> str:
        _, tag_attr = self.tags[tag]
        path = PathBuilder(link).make_save_path(self.resource_folder)
        resource[tag_attr] = path
        return path

    def record_resources(self, tag: str, path: str,
                         data: [str, requests.models.Response]) -> str:
        tag_name, tag_attr = self.tags[tag]
        path_to_save = os.path.join(self.save_path, path)
        _file_worker = FileWorker(data, path_to_save)
        recorder = _file_worker.record_image if tag_name == 'img' else \
            _file_worker.record_resource
        recorder()
        return path_to_save

    def download_all(self):

        make_dir(self.resource_folder)
        logging.info('Download image!')
        self.download_resources('img')
        self.download_resources('link')
        self.download_resources('script')
        FileWorker(self.data.prettify(),
                   self.main_file_path).record_html()


def checker(tag, res_path, webpage_link):
    if tag == 'img':
        check1 = check_image_extension(res_path)
        check2 = domain_check(res_path, webpage_link)
        return all((check1, check2))
    return domain_check(res_path, webpage_link)


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
    return True if web_page_parse.netloc == picture_link_parse.netloc \
        else False


def make_dir(path):
    try:
        if os.path.exists(path):
            pass
        logging.info('Creating a folder for local resources')
        os.mkdir(path)
    except OSError:
        logging.error('it is not possible to create a folder in this path')
        sys.exit(2)
