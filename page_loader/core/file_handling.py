from page_loader.core.dataclasses import RecordingData
FORMAT_FILE = '.html'


class FileWorker:

    def __init__(self, recording_data: RecordingData):
        self.data = recording_data.data
        self.path_to_save_data = recording_data.path_to_save_data

    def record_image(self) -> None:
        with open(self.path_to_save_data, 'wb') as image:
            for chunk in self.data.iter_content(chunk_size=1000):
                image.write(chunk)

    def record_html(self) -> None:
        with open(self.path_to_save_data, 'w') as file:
            file.write(self.data)

    def record_resource(self) -> None:
        with open(self.path_to_save_data, 'w') as resource:
            resource.write(self.data)
