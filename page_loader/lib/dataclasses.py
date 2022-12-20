from typing import NamedTuple
from typing import Literal


class ArgumentParser(NamedTuple):
    """Cli arguments. Url for download page, command to specify path to
    save directory"""
    url: Literal['url']
    save_directory_short: Literal['-o']
    save_directory_long: Literal['--output']
