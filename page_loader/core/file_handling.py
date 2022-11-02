from page_loader.core.dataclasses import RecordingData

FORMAT_FILE = '.html'


class FileWorker:
    """A class for working with files. Writes html files,
    local resources and byte files"""
    def __init__(self, recording_data: RecordingData):
        self.recording_data = recording_data

    def save_bytes_data(self) -> None:
        with open(self.recording_data.path_to_save_data, 'wb') as image:
            image.write(self.recording_data.data)

    def save_text_data(self) -> None:
        with open(self.recording_data.path_to_save_data, 'w') as file:
            file.write(self.recording_data.data)
