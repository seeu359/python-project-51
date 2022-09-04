import requests
import os
import re

FORMAT = '.html'


def get_format_path(path, save_path):
    template = re.findall(r'http://|https://[\da-zA-Z-.]+\.[a-zA-Z]'
                          r'+/[\w/-]+\.\w+', path)
    if len(template) != 0:
        not_format_path = os.path.splitext(''.join(template))[0]
        delete_scheme = re.sub(r'https://|http://', '', not_format_path)
        replace_dash = re.sub(r'[^a-zA-Z\d]', '-', delete_scheme)
        path_to_save = os.path.join(save_path, replace_dash)
        return path_to_save + '.html'
    else:
        not_format_path = path[0:-1] if path.endswith('/') else path
        delete_scheme = re.sub(r'https://|http://', '', not_format_path)
        replace_dash = re.sub(r'[^a-zA-Z\d]', '-', delete_scheme)
        path_to_save = os.path.join(save_path, replace_dash)
        return path_to_save + '.html'


def get_link_data(link):
    return requests.get(link).text


def download(link, save_path=os.getcwd()):
    path_to_save = get_format_path(link, save_path)
    with open(path_to_save, 'w') as html_file:
        html_file.write(get_link_data(link))
    return path_to_save
