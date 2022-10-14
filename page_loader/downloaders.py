import bs4.element
import requests
import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.file_handling import FileWorker
from page_loader.link_handling import PathBuilder
from page_loader.dataclasses import DownloadInformation, RecordingData, TagType
from progress.bar import ShadyBar

TAGS = {'img': ('img', 'src'),
        'link': ('link', 'href'),
        'script': ('script', 'src')}

FOLDER_SUFFIX = '_files'
FORMAT_FILE = '.html'


class Downloaders:

    def __init__(self, download_information: DownloadInformation,
                 webpage_data: str):
        self.link = download_information.link
        self.path_to_save_directory = \
            download_information.path_to_save_directory
        self.webpage_data = webpage_data
        self.format_webpage_link = PathBuilder(self.link).format_webpage_link()
        self.data = BeautifulSoup(self.webpage_data, 'html.parser')
        self.main_file_path = os.path.join(
            self.path_to_save_directory,
            self.format_webpage_link) + FORMAT_FILE
        self.resource_folder = os.path.join(
            self.path_to_save_directory,
            self.format_webpage_link) + FOLDER_SUFFIX

    @staticmethod
    def get_image_data(link: str) -> requests.models.Response:
        return requests.get(link, stream=True)

    @staticmethod
    def get_text_data(link: str) -> str:
        return requests.get(link).text

    def get_resources_lst(self, tag: TagType) -> list[bs4.ResultSet]:
        tag_name, tag_attr, _ = tag.value
        resources = self.data.find_all(tag_name, {tag_attr: True})
        resources_list = _checker(resources, tag_name, tag_attr, self.link)
        logging.info(f'{resources_list}')
        return resources_list

    def download_resources(self, tag: TagType) -> None:
        tag_name, tag_attr, tag_message = tag.value
        resource_loader = self.get_image_data if tag_name == 'img' else \
            self.get_text_data
        resources_list = self.get_resources_lst(tag)
        with ShadyBar(f'Downloading {tag_message}:', max=len(resources_list)) \
                as bar:
            for res in resources_list:
                resource = res[tag_attr]
                link = PathBuilder(self.link).build_link(resource)
                resource_data = resource_loader(link)
                local_resource_path = _change_path_in_html(
                    link, res, tag_attr, self.resource_folder)
                _record_resources(tag_name, local_resource_path, resource_data,
                                  self.path_to_save_directory)
                bar.next()

    def download_all(self) -> None:

        _make_dir(self.resource_folder)
        self.download_resources(TagType.IMG)
        self.download_resources(TagType.LINK)
        self.download_resources(TagType.SCRIPT)
        recording_data = RecordingData(data=self.data.prettify(),
                                       path_to_save_data=self.main_file_path)
        FileWorker(recording_data).record_html()


def _checker(resources_list: bs4.ResultSet, tag_name: str, tag_attr: str,
             webpage_link: str) -> bs4.ResultSet:
    if tag_name == 'img':
        for resource in resources_list:
            resource_path = resource[tag_attr]
            if not all((_check_image_extension(resource_path),
                        _check_domain(resource_path, webpage_link))):
                resources_list.remove(resource)
    elif tag_name != 'img':
        for resource in resources_list:
            resource_path = resource[tag_attr]
            if not _check_domain(resource_path, webpage_link):
                resources_list.remove(resource)
    return resources_list


def _check_image_extension(path):
    _, extension = os.path.splitext(path)
    if extension == '.png' or extension == '.jpeg':
        return True
    return False


def _check_domain(resource_link, web_page):
    picture_link_parse = urlparse(resource_link)
    web_page_parse = urlparse(web_page)
    if not picture_link_parse.scheme:
        return True
    return True if web_page_parse.netloc == picture_link_parse.netloc \
        else False


def _change_path_in_html(link: str, resource: bs4.ResultSet, tag_attr: str,
                         resource_folder) -> str:
    path = PathBuilder(link).build_path_to_swap_in_html(resource_folder)
    resource[tag_attr] = path
    return path


def _record_resources(tag_name: str, local_resource_path: str,
                      data: str | requests.models.Response,
                      save_folder: str) -> str:
    path_to_save_data = os.path.join(save_folder, local_resource_path)
    recording_data = RecordingData(data=data,
                                   path_to_save_data=path_to_save_data)
    _file_worker = FileWorker(recording_data)
    recorder = _file_worker.record_image if tag_name == 'img' else \
        _file_worker.record_resource
    recorder()
    return path_to_save_data


def _make_dir(path):
    logging.info('Creating a folder for local resources')
    try:
        os.mkdir(path)
        logging.info('The directory has been created')
    except FileExistsError:
        logging.info('The directory already exists')
        pass
