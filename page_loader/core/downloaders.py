import requests
import os
from page_loader.log_config import logger
from bs4 import BeautifulSoup, ResultSet, SoupStrainer
from urllib.parse import urlparse
from page_loader.core.file_handling import FileWorker
from page_loader.core.link_handling import PathHandler
from page_loader.core.dataclasses import DownloadInformation, RecordingData, \
    Webpage, ImgTag, ScriptTag, LinkTag, Tags, ExceptionLogMessage
from typing import Union, Iterable
from progress.bar import ShadyBar
from page_loader.exceptions import ImageDownloadingError, \
    TextDataDownloadingError


class Downloaders:
    """
    Main class. Loads local resources by the tags specified in the Tags
    class. At the moment resources from Img, link, script tags are being
    downloaded. If necessary, you can add necessary tags to the Tags dataclass.
    Parsing a page with BeautifulSoup.
    The download_all method allows you to download all the tags specified in
    Tags
    """
    def __init__(self, download_information: DownloadInformation,
                 webpage: Webpage):
        self.download_info = download_information
        self.webpage_data = webpage
        self.format_webpage_link = PathHandler(
            self.download_info.webpage_link).format_webpage_link()
        self.parse_data = BeautifulSoup(self.webpage_data.webpage,
                                        'html.parser')

    @staticmethod
    def get_bytes_data(link: str) -> bytes:
        request_status_code: int = requests.get(link).status_code
        if request_status_code != 200:
            logger.error(f'{ExceptionLogMessage.IMAGE_DOWNLOAD_ERROR.value}'
                         f'{link}')
            raise ImageDownloadingError
        content = requests.get(link).content
        return content

    @staticmethod
    def get_text_data(link: str) -> str:
        request_status_code: int = requests.get(link).status_code
        if request_status_code != 200:
            logger.error(f'{ExceptionLogMessage.TEXT_DOWNLOAD_ERROR.value}'
                         f'{link}')
            raise TextDataDownloadingError
        return requests.get(link).text

    def get_resources_set(self, tag: type[[ImgTag], type[ScriptTag],
                                          type[LinkTag]]) -> ResultSet:
        resources = self.parse_data.find_all(tag.name, {tag.attr: True})
        resources_set: ResultSet = _resources_validator(
            resources, tag, self.download_info.webpage_link)
        return resources_set

    def download_resources(self, tags: Iterable[Tags]) -> None:
        for _tag in tags:
            tag = _tag.value
            resources_set = self.get_resources_set(tag)
            with ShadyBar(f'Downloading {tag.message}:',
                          max=len(resources_set)) as bar:
                for res in resources_set:
                    resource = res[tag.attr]
                    _, extension = os.path.splitext(resource)
                    link = PathHandler(
                        self.download_info.webpage_link).build_resource_link(
                        resource)
                    resource_data = self.get_bytes_data(link) if \
                        extension in ('.jpeg', '.jpg', '.png', '.css') \
                        else self.get_text_data(link)
                    local_resource_path = _change_path_in_html(
                        link, res, tag.attr,
                        self.download_info.path_to_resources_directory)
                    _record_resources(
                        local_resource_path, resource_data,
                        self.download_info.path_to_save_directory, extension)
                    bar.next()

    def download_all(self) -> None:

        self.download_resources(Tags)
        FileWorker(
            _get_recording_data_obj(
                self.parse_data.prettify(),
                self.download_info.path_to_main_html)).record_text_data()


def _resources_validator(resources_list: ResultSet,
                         tag: type[Union[ImgTag, ScriptTag, LinkTag]],
                         webpage_link: str) -> ResultSet:
    """
    Check resource link domain.
    If tag == img, additionally verifies img extension. Download only images
    with png, jpeg, jpg extension.
    :param resources_list: type[ResultSet]
    :param tag: type[ImgTag, ScriptTag, LinkTag]
    :param webpage_link: str
    :return: ResultSet
    """
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
                         tag_attr: str, resource_folder: str) -> str:
    path = PathHandler(link).build_path_to_swap_in_html(resource_folder)
    resource[tag_attr] = path
    return path


def _record_resources(local_resource_path: str,
                      data: str | bytes,
                      save_folder: str, extension: str) -> None:
    path_to_save_data = os.path.join(save_folder, local_resource_path)
    recording_data = _get_recording_data_obj(data, path_to_save_data)
    _file_worker = FileWorker(recording_data)
    recorder = _file_worker.record_bytes_data if \
        extension in ('.png', '.jpeg', '.jpg', '.css') else \
        _file_worker.record_text_data
    recorder()


def _get_recording_data_obj(data: str | bytes,
                            path_to_save_data: str) -> RecordingData:
    return RecordingData(data=data, path_to_save_data=path_to_save_data)
