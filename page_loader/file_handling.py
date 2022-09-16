FORMAT_FILE = '.html'


class FileWorker:

    def __init__(self, data, path):
        self.data = data
        self.path = path

    def record_image(self):
        with open(self.path, 'wb') as image:
            for chunk in self.data.iter_content(chunk_size=1000):
                image.write(chunk)

    def record_html(self):
        with open(self.path, 'w') as file:
            file.write(self.data)

    def record_resource(self):
        with open(self.path, 'w') as resource:
            resource.write(self.data)
