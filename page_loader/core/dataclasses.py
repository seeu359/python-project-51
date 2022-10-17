from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
from typing import Literal


@dataclass
class Webpage:
    """The dataclass is an ordinary string. Created for clearer understanding
    of the returned data and further manipulations with it."""
    webpage: str


class DownloadInformation(NamedTuple):
    """Main info for download and save html page, make resource folder etc"""
    webpage_link: str
    path_to_save_directory: str
    path_to_resources_directory: str
    path_to_main_html: str


class ArgumentParser(NamedTuple):
    """Cli arguments. Link for download page, command to specify path to
    save directory"""
    link: Literal['link']
    save_directory_short: Literal['-o']
    save_directory_long: Literal['--output']


class RecordingData(NamedTuple):
    """Data for recording, path to save data"""
    data: str or bytes
    path_to_save_data: str


class ImgTag(NamedTuple):
    """Basic information required for parsing the IMG tag"""
    name = 'img'
    attr = 'src'
    message = 'images'


class LinkTag(NamedTuple):
    """Basic information required for parsing the Link tag"""
    name = 'link'
    attr = 'href'
    message = 'links'


class ScriptTag(NamedTuple):
    """Basic information required for parsing the Script tag"""
    name = 'script'
    attr = 'src'
    message = 'scripts'


class Tags(Enum):
    """A class for iterating basic tags"""
    IMG = ImgTag
    SCRIPT = ScriptTag
    LINK = LinkTag


class FileSuffixes(Enum):
    """FIle suffixes: additions for the folder name with the resources and
    main html file extension"""
    FOLDER_SUFFIX = '_files'
    HTML_FILE_SUFFIX = '.html'


class ExceptionLogMessage(Enum):
    """Exception message for log file"""
    CONNECTION_ERROR = 'Connection error! Error: '
    PAGE_NOT_AVAILABLE = 'Page not Available error. Status code is: '
    PERMISSION_DENIED = 'Can not create directory. Permission denied! Error: '
    FILE_EXIST_ERROR = 'The directory already exists. Error: '
    FILE_NOT_FOUND = 'No such directory. Error: '
    IMAGE_DOWNLOAD_ERROR = 'Downloading Image Error. Image link: '
    TEXT_DOWNLOAD_ERROR = 'Text Data Downloading Error.Resource link: '
    MISSING_SCHEMA = 'Missing scheme! Link: '


class UserMessage(Enum):
    """Exception message for user output message"""
    DOWNLOAD_SUCCESS = 'Page was downloaded!'
    DIRECTORY_CREATE_ERROR = 'Invalid path! Cannot create file in this path!'
    PERMISSION_DENIED = 'No write access to this folder!'
    FAILED_TO_LOAD = 'Failed to load page!'
    DATA_DOWNLOAD_ERROR = 'An error occurred while loading local resources!'
    MISSING_SCHEME = 'There is no scheme in the page address. ' \
                     'Example link: "https://'
