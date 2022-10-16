import pytest
import requests_mock
import pathlib
import tempfile
import requests
import os
from page_loader.core.downloaders import Downloaders, _checker, \
    _change_path_in_html, _record_resources
from page_loader.core.file_handling import FileWorker
from page_loader.core.link_handling import PathBuilder
from page_loader.loader import download
from page_loader.core.dataclasses import RecordingData, DownloadInformation, \
    TagType

TEST_LINK = 'http://test.com'
TEST_LINK2 = 'https://ru.hexlet.io/courses'
PATH = 'tests/fixtures'


def read_bytes_data(path):
    with open(path, 'rb') as f:
        file = f.read()
    return file


def read_text_data(path):
    with open(path) as f:
        file = f.read()
    return file


def test_main_func(html_fixture2):
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mock:
            mock.get(TEST_LINK, text=html_fixture2)
            path = download(TEST_LINK, tmp)
            path_to_dir = os.path.join(tmp, 'test-com_files')
            print(os.listdir(tmp))
            assert os.path.exists(path)
            assert os.path.isfile(path)
            assert os.path.isdir(path_to_dir)


def test_get_link_data(get_link_data_fixture):
    assert get_link_data_fixture == 'test'


def test_get_image_data(html_fixture):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mock:
            test_download_info = DownloadInformation(
                webpage_link=TEST_LINK, path_to_save_directory=tmp_dir,
                webpage_data=html_fixture, path_to_resources_directory=tmp_dir,
                path_to_main_html=tmp_dir)
            test_main_obj = Downloaders(test_download_info)
            content = read_bytes_data(os.path.join(PATH, 'image_fixture.png'))
            mock.get(TEST_LINK, content=content)
            image_data = test_main_obj.get_image_data(TEST_LINK)
            path = pathlib.Path(tmp_dir, 'test.png')
            recording_data = RecordingData(data=image_data,
                                           path_to_save_data=str(path))
            file_worker = FileWorker(recording_data)
            file_worker.record_image()
            image = read_bytes_data(path)
            assert image == requests.get(TEST_LINK).content


def test_change_path_in_html(test_bs_object):
    with tempfile.TemporaryDirectory() as tmp:
        img_result_set, _, _ = test_bs_object
        for img in img_result_set:
            old_path = img['src']
            new_path = _change_path_in_html(TEST_LINK, img, 'src', tmp)
            assert old_path != new_path


@pytest.mark.parametrize('extension, reader, path',
                         [('.css', read_bytes_data,
                           os.path.join(PATH, 'fixture_css_stylesheet.css')),
                          ('.html', read_text_data,
                           os.path.join(PATH, 'fixture_page.html'))])
def test_record_resource(extension, reader, path):
    with tempfile.TemporaryDirectory() as tmp:
        fixture_data = reader(path)
        local_resource_path = 'test_path.ext'
        _record_resources(local_resource_path, fixture_data, tmp, extension)
        test_file = reader(os.path.join(tmp, local_resource_path))
        path_to_file = os.path.join(tmp, local_resource_path)
        assert os.path.isfile(path_to_file)
        assert test_file == fixture_data


@pytest.mark.parametrize('file, input_value, expected',
                         [('fixture_for_img.html', TagType.IMG, 1),
                          ('fixture_for_link.html', TagType.LINK, 2),
                          ('fixture_for_script.html', TagType.SCRIPT, 1)]
                         )
def test_get_resources_set(file, input_value, expected):
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_data = read_text_data(os.path.join(PATH, file))
        download_information = DownloadInformation(
            webpage_link=TEST_LINK, path_to_save_directory=tmp_dir,
            webpage_data=test_data, path_to_resources_directory=tmp_dir,
            path_to_main_html=tmp_dir)
        test_obj = Downloaders(download_information)
        assert len(test_obj.get_resources_lst(input_value)) == expected


@pytest.mark.parametrize('index, tag_name, tag_attr, expected,',
                         [(0, 'img', 'src', 1),
                          (1, 'link', 'href', 2),
                          (2, 'script', 'src', 1)]
                         )
def test_is_true_domain(index, tag_name, tag_attr, expected, test_bs_object):
    resource_set = test_bs_object[index]
    result_set = _checker(resource_set, tag_name, tag_attr, TEST_LINK2)
    assert len(result_set) == expected


@pytest.mark.parametrize('link, expected',
                         [('test/file/path.png',
                           'folder_files/test-file-path.png'),
                          ('test/file/path',
                           'folder_files/test-file-path.html')]
                         )
def test_build_path_to_swap_in_html(link, expected):
    test_obj = PathBuilder(link)
    folder = 'main/folder_files'
    assert test_obj.build_path_to_swap_in_html(folder) == expected


@pytest.mark.parametrize('link, file_path, expected',
                         [(TEST_LINK, 'http://test.com/file/file2.png',
                           'http://test.com/file/file2.png'),
                          (TEST_LINK, 'file/file2.png',
                           'http://test.com/file/file2.png')]
                         )
def test_build_link(link, file_path, expected):
    test_obj = PathBuilder(link)
    assert test_obj.build_resource_link(file_path) == expected
