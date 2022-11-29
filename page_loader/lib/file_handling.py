from page_loader.lib.dataclasses import RecordingData
from page_loader.lib.exceptions import FileRecordingError
from page_loader.lib.exception_messages import FILE_SAVING_ERORR


def save_data(recording_data: RecordingData, record_mode: str) -> None:
    with open(recording_data.path_to_save_data, record_mode) as data:
        try:
            data.write(recording_data.data)
        except IOError as e:
            raise FileRecordingError(FILE_SAVING_ERORR) from e
