from page_loader.lib.exceptions import FileRecordingError
from page_loader.lib.exception_messages import FILE_SAVING_ERORR


def save_data(data: str | bytes, path_to_save: str, record_mode: str) -> None:
    with open(path_to_save, record_mode) as file:
        try:
            file.write(data)
        except IOError as e:
            raise FileRecordingError(FILE_SAVING_ERORR) from e
