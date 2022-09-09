import os

FOLDER_SUFFIX = '_files'


def record_image(save_path, request):
    with open(save_path, 'wb') as picture:
        for chunk in request.iter_content(chunk_size=1000):
            picture.write(chunk)


def make_dir(link, save_path):
    path_to_folder = os.path.join(save_path, link) + FOLDER_SUFFIX
    if os.path.exists(path_to_folder):
        return path_to_folder
    os.mkdir(path_to_folder)
    return path_to_folder
