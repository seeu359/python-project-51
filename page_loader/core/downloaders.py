import requests
import os
from page_loader.log_config import logger
from bs4 import BeautifulSoup, ResultSet, SoupStrainer
from urllib.parse import urlparse
from page_loader.core.file_handling import FileWorker
from page_loader.core.link_handling import PathBuilder
from page_loader.core.dataclasses import DownloadInformation, RecordingData, \
    Webpage, ImgTag, ScriptTag, LinkTag
from typing import Union
from progress.bar import ShadyBar
from page_loader.exceptions import ImageDownloadingError, \
    TextDataDownloadingError


class Downloaders:

    def __init__(self, download_information: DownloadInformation,
                 webpage: Webpage):
        self.download_info = download_information
        self.webpage_data = webpage
        self.format_webpage_link = PathBuilder(
            self.download_info.webpage_link).format_webpage_link()
        self.parse_data = BeautifulSoup(self.webpage_data.webpage,
                                        'html.parser')

    @staticmethod
    def get_bytes_data(link: str) -> bytes:
        request_status_code = requests.get(link).status_code
        if request_status_code != 200:
            logger.error(f'Downloading Image Error. Image link: {link}')
            raise ImageDownloadingError
        content = requests.get(link).content
        return content

    @staticmethod
    def get_text_data(link: str) -> str:
        request_status_code = requests.get(link).status_code
        if request_status_code != 200:
            logger.error(f'Text Data Downloading Error. '
                         f'Resource link: {link}')
            raise TextDataDownloadingError
        return requests.get(link).text

    def get_resources_lst(self, tag: type[Union[ImgTag, ScriptTag, LinkTag]]) \
            -> list[ResultSet]:
        resources = self.parse_data.find_all(tag.name,
                                             {tag.attr: True})
        resources_list = _resources_validator(resources, tag,
                                              self.download_info.webpage_link)
        return resources_list

    def download_resources(
            self, tag: type[Union[ImgTag, ScriptTag, LinkTag]]) -> None:
        resources_list = self.get_resources_lst(tag)
        with ShadyBar(f'Downloading {tag.message}:', max=len(resources_list)) \
                as bar:
            for res in resources_list:
                resource = res[tag.attr]
                _, extension = os.path.splitext(resource)
                link = PathBuilder(
                    self.download_info.webpage_link).build_resource_link(
                    resource)
                resource_data = self.get_bytes_data(link) if \
                    extension in ('.jpeg', '.jpg', '.png', '.css') \
                    else self.get_text_data(link)
                local_resource_path = _change_path_in_html(
                    link, res, tag.attr,
                    self.download_info.path_to_resources_directory)
                _record_resources(local_resource_path, resource_data,
                                  self.download_info.path_to_save_directory,
                                  extension)
                bar.next()

    def download_all(self) -> None:

        self.download_resources(ImgTag)
        self.download_resources(LinkTag)
        self.download_resources(ScriptTag)
        FileWorker(
            _get_recording_data_obj(
                self.parse_data.prettify(),
                self.download_info.path_to_main_html)).record_html()


def _resources_validator(resources_list: ResultSet,
                         tag: type[Union[ImgTag, ScriptTag, LinkTag]],
                         webpage_link: str) -> ResultSet:
    processed_set = ResultSet(SoupStrainer())
    if tag.name == 'img':
        for resource in resources_list:
            resource_path = resource[tag.attr]
            if all((_check_image_extension(resource_path),
                    _is_true_domain(resource_path, webpage_link))):
                processed_set.append(resource)
    else:
        for resource in resources_list:
            resource_path = resource[tag.attr]
            if _is_true_domain(resource_path, webpage_link):
                processed_set.append(resource)
    return processed_set


def _check_image_extension(path: str) -> bool:
    _, extension = os.path.splitext(path)
    if extension in ('.png', '.jpeg', '.jpg'):
        return True
    return False


def _is_true_domain(resource_link: str, webpage_link: str) -> bool:
    picture_link_parse = urlparse(resource_link)
    web_page_parse = urlparse(webpage_link)
    if not picture_link_parse.scheme:
        return True
    return True if web_page_parse.netloc == picture_link_parse.netloc \
        else False


def _change_path_in_html(link: str, resource: ResultSet,
                         tag_attr: str, resource_folder) -> str:
    path = PathBuilder(link).build_path_to_swap_in_html(resource_folder)
    resource[tag_attr] = path
    return path


def _record_resources(local_resource_path: str,
                      data: str | bytes,
                      save_folder: str, extension: str) -> None:
    path_to_save_data = os.path.join(save_folder, local_resource_path)
    recording_data = _get_recording_data_obj(data, path_to_save_data)
    _file_worker = FileWorker(recording_data)
    recorder = _file_worker.record_image if \
        extension in ('.png', '.jpeg', '.jpg', '.css') else \
        _file_worker.record_resource
    recorder()


def _get_recording_data_obj(data: str | bytes,
                            path_to_save_data: str) -> RecordingData:
    return RecordingData(data=data, path_to_save_data=path_to_save_data)
