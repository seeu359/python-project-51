from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
from typing import Literal


@dataclass
class DownloadInformation:
    webpage_link: str
    path_to_save_directory: str
    webpage_data: str
    path_to_resources_directory: str
    path_to_main_html: str


class ArgumentParser(NamedTuple):
    link: Literal['link']
    save_directory_short: Literal['-o']
    save_directory_long: Literal['--output']


@dataclass
class RecordingData:
    data: str or bytes
    path_to_save_data: str


class TagType(Enum):
    IMG = ('img', 'src', 'images')
    LINK = ('link', 'href', 'links')
    SCRIPT = ('script', 'src', 'scripts')


class FileSuffixes(Enum):
    FOLDER_SUFFIX = '_files'
    HTML_FILE_SUFFIX = '.html'
