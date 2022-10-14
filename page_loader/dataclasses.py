from dataclasses import dataclass
from enum import Enum


@dataclass
class DownloadInformation:
    link: str
    path_to_save_directory: str


@dataclass
class RecordingData:
    data: str or bytes
    path_to_save_data: str


class TagType(Enum):
    IMG = ('img', 'src', 'images')
    LINK = ('link', 'href', 'links')
    SCRIPT = ('script', 'src', 'scripts')
