import pytest
import requests_mock
import pathlib
import tempfile
import requests
import os
from page_loader.downloaders import Downloaders, checker
from page_loader.file_handling import FileWorker
from page_loader.link_handling import PathBuilder
from page_loader.page_loader import download


TEST_LINK = 'http://test.com'
PATH = 'tests/fixtures'


def read_picture(path):
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
            path_to_file = os.path.join(tmp, 'test.html')
            path_to_dir = os.path.join(tmp, 'test_files')
            assert os.path.exists(path_to_file)
            assert os.path.isfile(path_to_file)
            assert os.path.isdir(path_to_dir)
            assert isinstance(path, str) is True


def test_get_link_data(get_link_data_fixture):
    assert get_link_data_fixture == 'test'


def test_get_image_data(html_fixture):
    test_data = html_fixture
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mock:
            obj = Downloaders(TEST_LINK, tmp, test_data)
            content = read_picture(os.path.join(PATH, 'image_fixture.png'))
            mock.get(TEST_LINK, content=content)
            image_data = obj.get_image_data(TEST_LINK)
            path = pathlib.Path(tmp, 'test.png')
            file_worker = FileWorker(image_data, path)
            file_worker.record_image()
            image = read_picture(path)
            assert image == requests.get(TEST_LINK).content


def test_change_path_in_html(test_bs_object):
    with tempfile.TemporaryDirectory() as tmp:
        link = 'https://page-loader.hexlet.repl.co/'
        test_html, test_img = test_bs_object
        test_obj = Downloaders(link, tmp, test_html)
        for img in test_img:
            old_path = img['src']
            new_path = test_obj.change_path_in_html(TEST_LINK, img,
                                                    'img')
            assert old_path != new_path


def test_record_recourse(html_fixture, css_fixture):
    with tempfile.TemporaryDirectory() as tmp:
        test_obj = Downloaders(TEST_LINK, tmp, html_fixture)
        data = css_fixture
        path = test_obj.record_resources('link', 'test_folder', data)
        temp_css_file = read_text_data(path)
        assert temp_css_file == css_fixture


@pytest.mark.parametrize('file, input_value, expected',
                         [('fixture_for_img.html', 'img', 1),
                          ('fixture_for_link.html', 'link', 2),
                          ('fixture_for_script.html', 'script', 2)]
                         )
def test_resource_lst(file, input_value, expected):
    with tempfile.TemporaryDirectory() as tmp:
        test_data = read_text_data(os.path.join(PATH, file))
        test_obj = Downloaders(TEST_LINK, tmp, test_data)
        assert len(test_obj.get_resources_lst(
            test_obj.tags[input_value])) == expected


@pytest.mark.parametrize('tag, res_path, expected,',
                         [('img', '/test/path.svg', False),
                          ('img', 'http://test.com/test/path.png', True),
                          ('link', 'https://ru.test.com', False),
                          ('script', '/hello/test/script.js', True)]
                         )
def test_checker(tag, res_path, expected):
    assert checker(tag, res_path, TEST_LINK) is expected


@pytest.mark.parametrize('link, expected',
                         [('test/file/path.png',
                           'folder_files/test-file-path.png'),
                          ('test/file/path',
                           'folder_files/test-file-path.html')]
                         )
def test_make_save_path(link, expected):
    test_obj = PathBuilder(link)
    folder = 'main/folder_files'
    assert test_obj.make_save_path(folder) == expected


@pytest.mark.parametrize('link, file_path, expected',
                         [(TEST_LINK, 'http://test.com/file/file2.png',
                           'http://test.com/file/file2.png'),
                          (TEST_LINK, 'file/file2.png',
                           'http://test.com/file/file2.png')]
                         )
def test_build_link(link, file_path, expected):
    test_obj = PathBuilder(link)
    assert test_obj.build_link(file_path) == expected
