import requests
import os
from page_loader.lib.logs.log_config import logger
from bs4 import BeautifulSoup, ResultSet, SoupStrainer
from urllib.parse import urlparse
from page_loader.lib.file_handling import FileWorker
from page_loader.lib.url_handling import build_resource_url, PathHandler
from page_loader.lib.dataclasses import RecordingData, ImgTag, ScriptTag, \
    LinkTag, Tags
from page_loader.lib import exception_messages
from typing import Union, Iterable
from progress.bar import ShadyBar
from page_loader.lib.exceptions import ResourceDownloadError, HttpRequestError
from requests.exceptions import ConnectionError, InvalidSchema, \
    RequestException, HTTPError, URLRequired, TooManyRedirects, Timeout


class Downloader:
    """
    Main class. Loads local resources by the tags specified in the Tags
    class. At the moment resources from Img, link, script tags are being
    downloaded. If necessary, you can add necessary tags to the Tags dataclass.
    Parsing a page with BeautifulSoup.
    The download_all method allows you to download all the tags specified in
    Tags
    """
    def __init__(self, url: str, path_to_save_directory: str,
                 path_to_resources_folder: str, path_to_main_html: str,
                 webpage: str):
        self.url = url
        self.path_to_save_directory = path_to_save_directory
        self.path_to_resources_folder = path_to_resources_folder
        self.path_to_main_html = path_to_main_html
        self.webpage_data = webpage
        self.parse_data = BeautifulSoup(self.webpage_data,
                                        'html.parser')

    def get_resources_set(self, tag: type[[ImgTag], type[ScriptTag],
                                          type[LinkTag]]) -> ResultSet:
        resources = self.parse_data.find_all(tag.name, {tag.attr: True})
        resources_set: ResultSet = _resources_validator(
            resources, tag, self.url)
        return resources_set

    def download_resources(self, tags: Iterable[Tags]) -> None:
        for _tag in tags:
            tag = _tag.value
            resources_set = self.get_resources_set(tag)
            with ShadyBar(f'Downloading {tag.message}:',
                          max=len(resources_set)) as bar:
                for res in resources_set:
                    resource_link = res[tag.attr]
                    _, extension = os.path.splitext(resource_link)

                    resource_url = build_resource_url(self.url, resource_link)

                    resource_data = get_bytes_data(resource_url) if \
                        extension in ('.jpeg', '.jpg', '.png', '.css') \
                        else get_text_data(resource_url)

                    local_resource_path = _change_path_in_html(
                        resource_url, res, tag.attr,
                        self.path_to_resources_folder)

                    _save_resources(
                        local_resource_path, resource_data,
                        self.path_to_save_directory, extension)
                    bar.next()

    def download_all(self) -> None:

        self.download_resources(Tags)

        recording_data = RecordingData(
            data=self.parse_data.prettify(),
            path_to_save_data=self.path_to_main_html)

        FileWorker(recording_data).save_text_data()


def make_request(url: str) \
        -> requests.models.Response:
    try:
        response = requests.get(url)

    except (ConnectionError, InvalidSchema, RequestException, HTTPError,
            URLRequired, TooManyRedirects, Timeout) as e:
        logger.error(f'{exception_messages.CONNECTION_ERROR}'
                     f'{e}')
        raise HttpRequestError

    request_status_code = response.status_code
    if request_status_code in (404, 500):
        logger.error(f'{exception_messages.RESOURCE_LOAD_ERROR}'
                     f'{request_status_code}')
        raise ResourceDownloadError
    return response


def get_bytes_data(url: str) -> bytes:
    data = make_request(url)
    return data.content


def get_text_data(url: str) -> str:
    data = make_request(url)
    return data.text


def _resources_validator(resources_list: ResultSet,
                         tag: type[Union[ImgTag, ScriptTag, LinkTag]],
                         url: str) -> ResultSet:
    """
    Check resource url domain.
    If tag == img, additionally verifies img extension. Download only images
    with png, jpeg, jpg extension.
    :param tag: type[ImgTag, ScriptTag, LinkTag]
    :param url: str
    :return: ResultSet
    :param resources_list: type[ResultSet]
    """
    processed_set = ResultSet(SoupStrainer())
    if tag.name == 'img':
        for resource in resources_list:
            resource_path = resource[tag.attr]
            if all((_check_image_extension(resource_path),
                    _is_true_domain(resource_path, url))):
                processed_set.append(resource)
    else:
        for resource in resources_list:
            resource_path = resource[tag.attr]
            if _is_true_domain(resource_path, url):
                processed_set.append(resource)
    return processed_set


def _check_image_extension(path: str) -> bool:
    _, extension = os.path.splitext(path)
    if extension in ('.png', '.jpeg', '.jpg'):
        return True
    return False


def _is_true_domain(resource_link: str, webpage_url: str) -> bool:
    picture_link_parse = urlparse(resource_link)
    webpage_url_parse = urlparse(webpage_url)
    if not picture_link_parse.scheme:
        return True
    return True if webpage_url_parse.netloc == picture_link_parse.netloc \
        else False


def _change_path_in_html(link: str, resource: ResultSet,
                         tag_attr: str, resource_folder: str) -> str:
    path = PathHandler(link).build_path_to_swap_in_html(resource_folder)
    resource[tag_attr] = path
    return path


def _save_resources(local_resource_path: str,
                    data: str | bytes,
                    save_folder: str, extension: str) -> None:
    path_to_save_data = os.path.join(save_folder, local_resource_path)

    recording_data = RecordingData(data=data,
                                   path_to_save_data=path_to_save_data)

    _file_worker = FileWorker(recording_data)
    recorder = _file_worker.save_bytes_data if \
        extension in ('.png', '.jpeg', '.jpg', '.css') else \
        _file_worker.save_text_data
    recorder()
