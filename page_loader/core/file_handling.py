from page_loader.core.dataclasses import RecordingData
FORMAT_FILE = '.html'


class FileWorker:

    def __init__(self, recording_data: RecordingData, extension):
        self.path_to_save_data = recording_data.path_to_save_data
        self.extension = extension
        if extension == '.css':
            self.data = str(recording_data.data)
        else:
            self.data = recording_data.data

    def record_image(self) -> None:
        with open(self.path_to_save_data, 'wb') as image:
            image.write(self.data)

    def record_html(self) -> None:
        with open(self.path_to_save_data, 'w') as file:
            file.write(self.data)

    def record_resource(self) -> None:
        with open(self.path_to_save_data, 'w') as resource:
            resource.write(self.data)
