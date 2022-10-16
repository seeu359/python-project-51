from page_loader.core.dataclasses import RecordingData
FORMAT_FILE = '.html'


class FileWorker:

    def __init__(self, recording_data: RecordingData):
        self.recording_data = recording_data

    def record_image(self) -> None:
        with open(self.recording_data.path_to_save_data, 'wb') as image:
            image.write(self.recording_data.data)

    def record_html(self) -> None:
        with open(self.recording_data.path_to_save_data, 'w') as file:
            file.write(self.recording_data.data)

    def record_resource(self) -> None:
        with open(self.recording_data.path_to_save_data, 'w') as resource:
            resource.write(self.recording_data.data)
