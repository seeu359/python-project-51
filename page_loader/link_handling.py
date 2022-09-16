from urllib.parse import urlparse
import furl
import re
import os
import pathlib

FORMAT_FILE = '.html'


class PathBuilder:

    def __init__(self, link):
        self.link = link

    def make_save_path(self, save_folder):
        body, extension = os.path.splitext(self.link)
        if not extension:
            extension = FORMAT_FILE
        delete_scheme_in_link = re.sub('http://|https://', '', body)
        replace_symbols_in_link = re.sub(r'[^a-zA-Z\d]', '-',
                                         delete_scheme_in_link)
        pure_path = pathlib.PurePath(save_folder).name
        return os.path.join(pure_path, replace_symbols_in_link) + extension

    def build_link(self, file_path):
        parse_img_path = urlparse(file_path)
        parse_webpage_link = urlparse(self.link)
        if parse_img_path.scheme:
            return file_path
        link_body = f'{parse_webpage_link.scheme}://' \
                    f'{parse_webpage_link.netloc}'
        collected_link = furl.furl(link_body).add(path=file_path)
        return str(collected_link)

    def format_link(self):
        parse_link = urlparse(self.link)
        link_without_scheme = ''.join(parse_link[1:])
        template = re.findall(r'[\da-zA-Z-.]+\.[a-zAZ]+/[@\w/-]+\.\w+',
                              link_without_scheme)
        not_format_link = link_without_scheme[0:-1] if \
            self.link.endswith('/') else link_without_scheme

        if len(template) == 0:
            format_link = re.sub(r'[^a-zA-Z\d]', '-', not_format_link)
            return format_link
        link_body, _ = os.path.splitext(not_format_link)
        format_link = re.sub(r'[^a-zA-Z\d]', '-', link_body)
        return format_link
