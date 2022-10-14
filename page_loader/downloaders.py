import requests
import os
import logging
from bs4 import BeautifulSoup, ResultSet
from urllib.parse import urlparse
from page_loader.file_handling import FileWorker
from page_loader.link_handling import PathBuilder
from page_loader.dataclasses import DownloadInformation, RecordingData, TagType
from progress.bar import ShadyBar
from page_loader.exceptions import ImageDownloadingError, \
    TextDataDownloadingError


class Downloaders:

    def __init__(self, download_information: DownloadInformation):
        self.webpage_link = download_information.webpage_link
        self.path_to_save_directory = \
            download_information.path_to_save_directory
        self.webpage_data = download_information.webpage_data
        self.path_to_resources_directory = \
            download_information.path_to_resources_directory
        self.path_to_main_html = download_information.path_to_main_html
        self.format_webpage_link = PathBuilder(
            self.webpage_link).format_webpage_link()
        self.parse_data = BeautifulSoup(self.webpage_data, 'html.parser')

    @staticmethod
    def get_image_data(link: str) -> requests.models.Response:
        request_status_code = requests.get(link).status_code
        if request_status_code != 200:
            logging.error(f'Downloading Image Error. Image link: {link}')
            raise ImageDownloadingError
        return requests.get(link, stream=True)

    @staticmethod
    def get_text_data(link: str) -> str:
        request_status_code = requests.get(link).status_code
        if request_status_code != 200:
            logging.error(f'Text Data Downloading Error. '
                          f'Resource link: {link}')
            raise TextDataDownloadingError
        return requests.get(link).text

    def get_resources_lst(self, tag: TagType) -> list[ResultSet]:
        tag_name, tag_attr, _ = tag.value
        resources = self.parse_data.find_all(tag_name, {tag_attr: True})
        resources_list = _checker(resources, tag_name, tag_attr,
                                  self.webpage_link)
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
                link = PathBuilder(self.webpage_link).build_link(resource)
                resource_data = resource_loader(link)
                local_resource_path = _change_path_in_html(
                    link, res, tag_attr, self.path_to_resources_directory)
                _record_resources(tag_name, local_resource_path, resource_data,
                                  self.path_to_save_directory)
                bar.next()

    def download_all(self) -> None:

        self.download_resources(TagType.IMG)
        self.download_resources(TagType.LINK)
        self.download_resources(TagType.SCRIPT)
        recording_data = RecordingData(
            data=self.parse_data.prettify(),
            path_to_save_data=self.path_to_main_html)
        FileWorker(recording_data).record_html()


def _checker(resources_list: ResultSet, tag_name: str, tag_attr: str,
             webpage_link: str) -> ResultSet:
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


def _change_path_in_html(link: str, resource: ResultSet, tag_attr: str,
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
