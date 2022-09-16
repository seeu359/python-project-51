import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import logging
from page_loader.file_handling import FileWorker
from page_loader.link_handling import PathBuilder


FOLDER_SUFFIX = '_files'
FORMAT_FILE = '.html'


class Downloaders:

    tags = {'img': ('img', 'src'),
            'link': ('link', 'href'),
            'script': ('script', 'src')}

    def __init__(self, link, save_path=os.getcwd()):
        self.link = link
        self.format_link = PathBuilder(link).format_link()
        self.save_path = save_path
        self.main_file_path = os.path.join(self.save_path,
                                           self.format_link) + FORMAT_FILE
        self.link_data = BeautifulSoup(self.get_link_data(), 'html.parser')
        self.resource_folder = os.path.join(save_path,
                                            self.format_link) + FOLDER_SUFFIX

        make_dir(self.resource_folder)

    def get_link_data(self):
        logging.info(f'request {self.link}')
        return requests.get(self.link).text

    @staticmethod
    def get_image_data(link):
        return requests.get(link, stream=True)

    @staticmethod
    def get_text_data(link):
        return requests.get(link).text

    def get_resources_lst(self, tag):
        tag_name, tag_attr = tag
        resources = self.link_data.find_all(tag_name, {tag_attr: True})
        return resources

    def download_resources(self, tag):
        resource_loader = self.get_image_data if tag == 'img' else \
            self.get_text_data
        tag_name, tag_attr = self.tags[tag]
        for resource in self.get_resources_lst(self.tags[tag]):
            res = resource[tag_attr]
            if checker(tag, res, self.link):
                link = PathBuilder(self.link).build_link(res)
                resource_data = resource_loader(link)
                path = PathBuilder(link).make_save_path(self.resource_folder)
                resource[tag_attr] = path
                path_to_save = os.path.join(self.save_path, path)
                _file_worker = FileWorker(resource_data, path_to_save)
                recorder = _file_worker.record_image if tag == 'img' else \
                    _file_worker.record_resource
                recorder()

    def download_all(self):

        self.download_resources('img')
        self.download_resources('link')
        self.download_resources('script')
        FileWorker(self.link_data.prettify(),
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
    else:
        return True if web_page_parse.netloc == picture_link_parse.netloc \
            else False


def make_dir(path):
    if os.path.exists(path):
        return None
    logging.info('Creating a folder for local resources')
    os.mkdir(path)
