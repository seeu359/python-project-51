from dataclasses import dataclass
from enum import Enum


@dataclass
class DownloadInformation:
    webpage_link: str
    path_to_save_directory: str
    webpage_data: str
    path_to_resources_directory: str
    path_to_main_html: str


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
