from page_loader.lib.dataclasses import RecordingData
from page_loader.lib.exceptions import FileRecordingError
from page_loader.lib.exception_messages import FILE_SAVING_ERORR

FORMAT_FILE = '.html'


class FileWorker:
    """A class for working with files. Writes html files,
    local resources and byte files"""
    def __init__(self, recording_data: RecordingData):
        self.recording_data = recording_data

    def save_bytes_data(self) -> None:
        with open(self.recording_data.path_to_save_data, 'wb') as image:
            try:
                image.write(self.recording_data.data)
            except IOError as e:
                raise FileRecordingError(FILE_SAVING_ERORR) from e

    def save_text_data(self) -> None:
        with open(self.recording_data.path_to_save_data, 'w') as file:
            try:
                file.write(self.recording_data.data)
            except IOError as e:
                raise FileRecordingError(FILE_SAVING_ERORR) from e
