import requests
import os
import logging
from bs4 import BeautifulSoup, ResultSet, SoupStrainer
from urllib.parse import urlparse
from page_loader.core.file_handling import FileWorker
from page_loader.core.link_handling import PathBuilder
from page_loader.core.dataclasses import DownloadInformation, RecordingData, \
    TagType
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
    def get_image_data(link: str) -> bytes:
        request_status_code = requests.get(link).status_code
        if request_status_code != 200:
            logging.error(f'Downloading Image Error. Image link: {link}')
            raise ImageDownloadingError
        return requests.get(link).content

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
        resources_list = self.get_resources_lst(tag)
        with ShadyBar(f'Downloading {tag_message}:', max=len(resources_list)) \
                as bar:
            for res in resources_list:
                resource = res[tag_attr]
                _, extension = os.path.splitext(resource)
                resource_loader = self.get_image_data if \
                    extension in ('.jpeg', '.jpg', '.png', '.css') \
                    else self.get_text_data
                link = PathBuilder(self.webpage_link).build_resource_link(
                    resource)
                resource_data = resource_loader(link)
                local_resource_path = _change_path_in_html(
                    link, res, tag_attr, self.path_to_resources_directory)
                _record_resources(tag_name, local_resource_path, resource_data,
                                  self.path_to_save_directory, extension)
                bar.next()

    def download_all(self) -> None:

        self.download_resources(TagType.IMG)
        self.download_resources(TagType.LINK)
        self.download_resources(TagType.SCRIPT)
        recording_data = RecordingData(
            data=self.parse_data.prettify(),
            path_to_save_data=self.path_to_main_html)
        FileWorker(recording_data, '.html').record_html()


def _checker(resources_list: ResultSet, tag_name: str, tag_attr: str,
             webpage_link: str) -> ResultSet:
    processed_set = ResultSet(SoupStrainer())
    if tag_name == 'img':
        for resource in resources_list:
            resource_path = resource[tag_attr]
            if all((_check_image_extension(resource_path),
                    _is_true_domain(resource_path, webpage_link))):
                processed_set.append(resource)
    else:
        for resource in resources_list:
            resource_path = resource[tag_attr]
            if _is_true_domain(resource_path, webpage_link):
                processed_set.append(resource)
    return processed_set


def _check_image_extension(path: str) -> bool:
    _, extension = os.path.splitext(path)
    if extension == '.png' or extension in ('.jpeg', '.jpg'):
        return True
    return False


def _is_true_domain(resource_link: str, webpage_link: str) -> bool:
    picture_link_parse = urlparse(resource_link)
    web_page_parse = urlparse(webpage_link)
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
                      save_folder: str, extension) -> str:
    path_to_save_data = os.path.join(save_folder, local_resource_path)
    recording_data = RecordingData(data=data,
                                   path_to_save_data=path_to_save_data)
    _file_worker = FileWorker(recording_data, extension)
    recorder = _file_worker.record_image if tag_name == 'img' else \
        _file_worker.record_resource
    recorder()
    return path_to_save_data
