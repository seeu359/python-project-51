import pytest
import requests_mock
import pathlib
import tempfile
import os
from page_loader.downloaders import Downloaders, checker
from page_loader.file_handling import FileWorker
import requests


TEST_PATH = os.getcwd()
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


def test_get_link_data(get_link_data_fixture):
    assert get_link_data_fixture == 'test'


def test_get_image_data(read_html_fixture):
    test_data = read_html_fixture
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mock:
            obj = Downloaders(TEST_LINK, os.getcwd(), test_data)
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


def test_record_recourse(read_html_fixture, css_fixture):
    with tempfile.TemporaryDirectory() as tmp:
        test_obj = Downloaders(TEST_LINK, tmp, read_html_fixture)
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
    test_data = read_text_data(os.path.join(PATH, file))
    test_obj = Downloaders(TEST_LINK, os.getcwd(), test_data)
    assert len(test_obj.get_resources_lst(
        test_obj.tags[input_value])) == expected


@pytest.mark.parametrize('tag, res_path, webpage_link, expected,',
                         [('img', '/test/path.svg', TEST_LINK, False),
                          ('img', 'http://test.com/test/path.png',
                           TEST_LINK, True),
                          ('link', 'https://ru.test.com', TEST_LINK, False),
                          ('script', '/hello/test/script.js', TEST_LINK, True)]
                         )
def test_checker(tag, res_path, webpage_link, expected):
    assert checker(tag, res_path, webpage_link) is expected


