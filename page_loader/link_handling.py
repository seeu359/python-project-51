from urllib.parse import urlparse
import furl
import re
import os
import pathlib

FORMAT_FILE = '.html'


class PathBuilder:

    def __init__(self, link):
        self.link = link
        self.parse_link = urlparse(link)
        self.link_body, self.extension = os.path.splitext(link)
        self.processed_link = re.sub('http://|https://', '',
                                     self.link_body)

    def make_save_path(self, save_folder):
        if not self.extension:
            self.extension = FORMAT_FILE
        replace_symbols_in_link = re.sub(r'[^a-zA-Z\d]', '-',
                                         self.processed_link)
        pure_path = pathlib.PurePath(save_folder).name
        return os.path.join(pure_path,
                            replace_symbols_in_link) + self.extension

    def build_link(self, file_path):
        parse_img_path = urlparse(file_path)
        if parse_img_path.scheme:
            return file_path
        link_body = f'{self.parse_link.scheme}://' \
                    f'{self.parse_link.netloc}'
        collected_link = furl.furl(link_body).add(path=file_path)
        return str(collected_link)

    def format_link(self):
        not_format_link = self.processed_link[0:-1] if \
            self.link.endswith('/') else self.processed_link
        format_link = re.sub(r'[^a-zA-Z\d]', '-', not_format_link)
        return format_link
