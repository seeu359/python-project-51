from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
from typing import Literal


@dataclass
class Webpage:
    webpage: str


class DownloadInformation(NamedTuple):
    webpage_link: str
    path_to_save_directory: str
    path_to_resources_directory: str
    path_to_main_html: str


class ArgumentParser(NamedTuple):
    link: Literal['link']
    save_directory_short: Literal['-o']
    save_directory_long: Literal['--output']


class RecordingData(NamedTuple):

    data: str or bytes
    path_to_save_data: str


class ImgTag(NamedTuple):
    name = 'img'
    attr = 'src'
    message = 'images'


class LinkTag(NamedTuple):
    name = 'link'
    attr = 'href'
    message = 'links'


class ScriptTag(NamedTuple):
    name = 'script'
    attr = 'src'
    message = 'scripts'


class FileSuffixes(Enum):
    FOLDER_SUFFIX = '_files'
    HTML_FILE_SUFFIX = '.html'
