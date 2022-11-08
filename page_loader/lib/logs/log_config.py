import logging
import os


def _get_logfile_path() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'logs.log')


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(format='%(levelname)s :: %(asctime)s :: %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filename=_get_logfile_path(),
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
