import requests
from bs4 import BeautifulSoup
import os
import pathlib
from page_loader import link_handling as lh
from page_loader import file_handling as fh


def get_extension(link):
    _, extension = os.path.splitext(link)
    if extension:
        return extension
    return '.html'


def get_link_data(link):
    return requests.get(link).text


def get_link_pic(link):
    return requests.get(link, stream=True)


def get_local_resources(file_data, download_folder, link):
    handler = BeautifulSoup(file_data, 'html.parser')
    download_resources1 = get_image(handler, download_folder, link)
    download_resources2 = get_links(download_resources1, download_folder, link)
    download_resources3 = get_script(download_resources2, download_folder,
                                     link)
    file_data = download_resources3.prettify()
    return file_data


def get_image(data, download_folder, link,
              data_parser=get_link_pic, data_recorder=fh.record_image):
    image_list = data.find_all('img', {'src': True})
    for img in image_list:
        src = img['src']
        extension = get_extension(src)
        if (extension == '.png' or extension == '.jpg') and \
                lh.domain_check(src, link) is True:
            constructed_link = lh.make_source_link(link, src)
            format_link = lh.get_format_link(constructed_link)
            request = data_parser(constructed_link)
            save_path = os.path.join(download_folder, format_link) + extension
            pure_path = pathlib.PurePath(download_folder).name
            img['src'] = os.path.join(pure_path, format_link) + extension
            data_recorder(save_path, request)
    return data


def get_links(data, download_folder, link,
              data_parser=get_link_data, data_recorder=fh.record_resources):
    links_list = data.find_all('link', {'href': True})
    for tag_link in links_list:
        href = tag_link['href']
        extension = get_extension(href)
        if lh.domain_check(href, link):
            constructed_link = lh.make_source_link(link, href)
            format_link = lh.get_format_link(constructed_link)
            request = data_parser(constructed_link)
            save_path = os.path.join(download_folder, format_link) + extension
            pure_path = pathlib.PurePath(download_folder).name
            tag_link['href'] = os.path.join(pure_path, format_link) + extension
            data_recorder(save_path, request)
    return data


def get_script(data, download_folder, link,
               data_parser=get_link_data,
               data_recorder=fh.record_resources):
    scripts_list = data.find_all('script', {'src': True})
    for script in scripts_list:
        src = script['src']
        extension = get_extension(src)
        if lh.domain_check(src, link):
            constructed_link = lh.make_source_link(link, src)
            format_link = lh.get_format_link(constructed_link)
            request = data_parser(constructed_link)
            save_path = os.path.join(download_folder, format_link) + extension
            pure_path = pathlib.PurePath(download_folder).name
            script['src'] = os.path.join(pure_path, format_link) + extension
            data_recorder(save_path, request)
    return data
