import requests
import os
from page_loader.lib.logs.log_config import logger
from bs4 import BeautifulSoup, ResultSet, SoupStrainer
from urllib.parse import urlparse
from page_loader.lib.file_handling import save_data
from page_loader.lib.url_handling import build_resource_url, PathHandler
from page_loader.lib import exception_messages as em
from progress.bar import ShadyBar
from page_loader.lib.exceptions import ResourceDownloadError, \
    HttpRequestError, DirectoryCreationError
from requests import exceptions as exc


def download_resources(
        url: str,
        path_to_save_dir: str,
        path_to_resource_dir: str,
        path_to_main_html: str,
        data: str,
):
    soup = BeautifulSoup(data, 'html.parser')
    img, link, script = _get_resources(soup, url)
    _make_dir(path_to_resource_dir)
    _download_resources_from_tags(
        url,
        path_to_save_dir,
        path_to_resource_dir,
        img=img,
        link=link,
        script=script,
    )
    save_data(soup.prettify(), path_to_main_html, 'w')


def _download_resources_from_tags(
        url, path_to_save_dir, path_to_resource_dir, **kwargs
) -> None:
    for tag, resource_set in kwargs.items():
        attr = _get_attr(tag)
        _handle_tag(
            url,
            path_to_save_dir,
            path_to_resource_dir,
            attr,
            resource_set,
        )


def _handle_tag(
        url: str,
        path_to_save_dir: str,
        path_to_resource_dir: str,
        attr: str,
        resource_set: ResultSet,
):
    with ShadyBar('Downloading resources:', max=len(resource_set)) as bar:
        for res in resource_set:
            resource_link = res[attr]
            _, extension = os.path.splitext(resource_link)
            resource_url = build_resource_url(url, resource_link)

            resource_data = _get_bytes_data(resource_url) \
                if extension in ('.jpeg', '.jpg', '.png', '.css') \
                else _get_text_data(resource_url)

            resource_path_in_html = PathHandler(resource_url).\
                build_path_to_swap_in_html(path_to_resource_dir)

            res[attr] = resource_path_in_html
            _save_resources(
                resource_path_in_html, resource_data,
                path_to_save_dir, extension,
            )
            bar.next()


def _get_attr(tag: str) -> str:
    mapper = {
        'img': 'src',
        'link': 'href',
        'script': 'src',
    }
    return mapper[tag]


def _make_dir(path: str) -> None:
    try:
        os.mkdir(path)
    except PermissionError as e:
        logger.error(f'{em.PERMISSION_DENIED}{e}')
        raise DirectoryCreationError(em.USER_PERMISSION_DENIED) from e
    except FileExistsError as e:
        logger.error(f'{em.FILE_EXIST_ERROR}{e}')
        raise DirectoryCreationError(em.USER_DIRECTORY_EXIST) from e
    except FileNotFoundError as e:
        logger.error(f'{em.FILE_NOT_FOUND}{e}')
        raise DirectoryCreationError(em.DIRECTORY_CREATE_ERROR) from e


def _get_resources(soup: BeautifulSoup, url: str) -> tuple[ResultSet, ...]:
    img = _resources_validator(soup.select('img[src]'), 'img', 'src', url)
    link = _resources_validator(
        soup.select('link[href]'), 'link', 'href', url
    )
    script = _resources_validator(
        soup.select('script[src]'), 'script', 'src', url
    )
    return img, link, script


def make_request(url: str) \
        -> requests.models.Response:
    try:
        response = requests.get(url)

    except (
            ConnectionError, exc.InvalidSchema, exc.RequestException,
            exc.HTTPError, exc.URLRequired, exc.TooManyRedirects, exc.Timeout
    ) as e:
        logger.error(f'{em.CONNECTION_ERROR}'
                     f'{e}')
        raise HttpRequestError(em.FAILED_TO_LOAD)

    request_status_code = response.status_code
    if request_status_code != 200:
        logger.error(f'{em.RESOURCE_LOAD_ERROR}'
                     f'{request_status_code}')
        raise ResourceDownloadError(em.RESOURCE_LOAD_ERROR)
    return response


def _get_bytes_data(url: str) -> bytes:
    data = make_request(url)
    return data.content


def _get_text_data(url: str) -> str:
    data = make_request(url)
    return data.text


def _resources_validator(resources_list: ResultSet,
                         tag: str,
                         attr: str,
                         url: str,
                         ) -> ResultSet:
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
    if tag == 'img':
        for resource in resources_list:
            resource_path = resource[attr]
            if all((_check_image_extension(resource_path),
                    _is_true_domain(resource_path, url))):
                processed_set.append(resource)
    else:
        for resource in resources_list:
            resource_path = resource[attr]
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


def _save_resources(local_resource_path: str,
                    data: str | bytes,
                    save_folder: str,
                    extension: str,
                    ) -> None:
    path_to_save_data = os.path.join(save_folder, local_resource_path)
    record_mode = 'wb' if extension in ('.png', '.jpeg', '.jpg', '.css') else \
        'w'
    save_data(data, path_to_save_data, record_mode)
